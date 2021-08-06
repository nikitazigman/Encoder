import time
import threading

from gpiozero import RotaryEncoder
from gpiozero.pins.mock import MockFactory, MockPin


def foo():
    rotor = RotaryEncoder(21, 20, max_steps=0, pin_factory=MockFactory())

    while True:
        print(rotor.steps)
        time.sleep(0.5)


if __name__ == "__main__":
    thread = threading.Thread(target=foo)
    thread.start()

    mock_factory = MockFactory()
    led21:MockPin = mock_factory.pin(21)
    led20:MockPin = mock_factory.pin(20)
    # led21 = LED(21)
    # led20 = LED(20)
    
    
    for _ in range(2):
        led21.drive_high()
        time.sleep(0.002)
        led20.drive_high()
        time.sleep(0.002)
        led21.drive_low()
        time.sleep(0.002)
        led20.drive_low()
        time.sleep(0.002)
    