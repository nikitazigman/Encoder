import time
import threading

from gpiozero import RotaryEncoder
from gpiozero.pins.mock import MockFactory, MockPin
from encoder import Encoder, EncoderInterface, EncoderData
from fabrics import ValueType, RangeType, value_converter_fabric, range_converter_fabric

settings = {
    "range_converter": range_converter_fabric(RangeType.minus_half_to_half),
    "value_converter": value_converter_fabric(ValueType.degree),
    "pin_a": 20,            
    "pin_b": 21,
    "duration": 0.1, # 100 ms
    "period": 360,
    "virtual": True,
}
class_settings = EncoderData(**settings)

def foo():
    # rotor = RotaryEncoder(21, 20, max_steps=0, pin_factory=MockFactory())
    encoder = Encoder(class_settings)
    while True:
        print(f"{encoder.position=}")
        print(f"{encoder.velocity=}")
        print(f"{encoder.direction=}")
        time.sleep(0.5)


if __name__ == "__main__":
    thread = threading.Thread(target=foo)
    thread.start()

    mock_factory = MockFactory()
    led21:MockPin = mock_factory.pin(21)
    led20:MockPin = mock_factory.pin(20)
   
    for _ in range(2):
        led21.drive_high()
        time.sleep(0.002)
        led20.drive_high()
        time.sleep(0.002)
        led21.drive_low()
        time.sleep(0.002)
        led20.drive_low()
        time.sleep(0.002)
    