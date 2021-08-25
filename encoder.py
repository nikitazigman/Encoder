from abc import ABC, abstractmethod
from time import time
from threading import Lock, Timer
from typing import Union, Type

from gpiozero import RotaryEncoder
from gpiozero.pins.mock import MockFactory
from pydantic import BaseModel


if __package__:
    from .range_converter import RangeConverterInterface
    from .value_converter import ValueConveterInterface
else:
    from range_converter import RangeConverterInterface
    from value_converter import ValueConveterInterface


class EncoderData(BaseModel):
    range_converter: Type[RangeConverterInterface]
    value_converter: Type[ValueConveterInterface]
    pin_a: int
    pin_b: int
    duration: float #sec
    period: int
    virtual: bool = False
    bounce_time: Union[float, None] = None #ms 
    reverse: bool = False 


class EncoderInterface(ABC):
    """Abstract Interface for Encoders Classes"""

    @property
    @abstractmethod
    def direction(self) -> int:
        """return direction +1 or -1"""
    
    @property
    @abstractmethod
    def position(self) -> float:
        """return position of an encoder (cnt, degree or something else)"""        
    
    @property
    @abstractmethod
    def velocity(self) -> float:
        """return angular_speed"""


class Encoder(EncoderInterface):
    """provide the value quadrature encoder

        the class is using Rpi.GPIO and interruption to handle encoder's events
        you need to setup A and B pins, optionally you can define jitter filter(ms), switch direction.
    """

    def __init__(self, encoder_data: EncoderData):
        if type(encoder_data) is not EncoderData:
            raise TypeError('encoder_data has to have the EncoderData type')

        self._position = 0
        self._velocity = 0
        self._direction = 0
        self._previous_position = 0
        
        self._virtual = encoder_data.virtual
        self._factory = None if not self._virtual else MockFactory()
        self._range_converter: RangeConverterInterface = encoder_data.range_converter()
        self._value_converter: ValueConveterInterface = encoder_data.value_converter()
        self._period_cnt = encoder_data.period
        self._duration = encoder_data.duration
        self._bounce_time = encoder_data.bounce_time

        if not encoder_data.reverse:
            self._pin_a, self._pin_b = encoder_data.pin_a, encoder_data.pin_b
        else: 
            self._pin_a, self._pin_b = encoder_data.pin_b, encoder_data.pin_a

        self._lock = Lock()

        self._encoder = RotaryEncoder(
            self._pin_a, 
            self._pin_b,
            max_steps= 0, 
            bounce_time=self._bounce_time,
            pin_factory= self._factory
        )
        self._encoder.steps = 1       
        self._start_timer()

    def __del__(self):
        self._lock.acquire()
        
    def _start_timer(self):
        self._thread = Timer(self._duration, self._timer_callback, args=[time()])
        self._thread.start()

    def _timer_callback(self, previous_time: float):
        # print("i'm in thread")
        with self._lock:
            # print("i'm in thread2 ")
            current_position = self._encoder.steps
            current_time = time()

            delta_position = current_position - self._previous_position
            delta_time = current_time - previous_time

            self._velocity = delta_position/delta_time

            self._previous_position = current_position

            self._start_timer()
    
    @property
    def position(self) -> float:
        """it first convert it to the given range and then convert it to the given measuremnts type"""

        position = self._range_converter.convert_range(self._encoder.steps, self._period_cnt)
        return self._value_converter.convert(position, self._period_cnt)
    
    @property
    def direction(self) -> int:
        velocity = self.velocity
        
        if velocity > 0:
            self._direction = 1
        
        elif velocity < 0:
            self._direction = -1
        
        else:
            self._direction = 0

        return self._direction
    
    @property
    def velocity(self) -> float:
        
        with self._lock:
            velocity = self._velocity
        
        return self._value_converter.convert(velocity, self._period_cnt)


