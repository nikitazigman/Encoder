from abc import ABC, abstractmethod
from time import time
from threading import Event, Thread, Lock
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
    period: int
    virtual: bool = False
    bounce_time: Union[float, None] = None #ms 
    reverse: bool = False 


class EncoderInterface(ABC):
    """Abstract Interface for Encoders Classes"""
   
    @property
    @abstractmethod
    def position(self) -> float:
        """return position of an encoder (cnt, degree or something else)"""        
    

class Encoder(EncoderInterface):
    """provide the value quadrature encoder

        the class is using Rpi.GPIO and interruption to handle encoder's events
        you need to setup A and B pins, optionally you can define jitter filter(ms), switch direction.
    """

    def __init__(self, encoder_data: EncoderData):
        if type(encoder_data) is not EncoderData:
            raise TypeError('encoder_data has to have the EncoderData type')
        
        self._virtual = encoder_data.virtual
        self._factory = None if not self._virtual else MockFactory()
        self._range_converter: RangeConverterInterface = encoder_data.range_converter()
        self._value_converter: ValueConveterInterface = encoder_data.value_converter()
        self._period_cnt = encoder_data.period
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
    
    @property
    def position(self) -> float:
        """it first convert it to the given range and then convert it to the given measuremnts type"""

        position = self._range_converter.convert_range(self._encoder.steps, self._period_cnt)
        return self._value_converter.convert(position, self._period_cnt)
    

