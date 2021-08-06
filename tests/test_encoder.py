import math
import time
import unittest
from unittest.mock import patch, call

from gpiozero.pins.mock import MockFactory, MockPin

from encoder import Encoder, EncoderInterface, EncoderData
from fabrics import ValueType, RangeType, value_converter_fabric, range_converter_fabric


class TestEncoder(unittest.TestCase):
    def setUp(self):
        settings = {
            "range_converter": range_converter_fabric(RangeType.minus_half_to_half),
            "value_converter": value_converter_fabric(ValueType.degree),
            "pin_a": 20,            
            "pin_b": 21,
            "duration": 0.1, # 100 ms
            "period": 360,
            "virtual": True,
        }
        self.settings = EncoderData(**settings)

        self.pin_a: MockPin = MockFactory().pin(20)
        self.pin_b: MockPin = MockFactory().pin(21)

        self.impulse_delay = 0.02 # sec

    def tearDown(self):
        MockFactory().close()
        # self.pin_a.close()
        # self.pin_b.close()

    def _send_cnt(self, cnt_number: int, impulse_delay: float):
        for _ in range(cnt_number + 1):
            self.pin_a.drive_high()
            time.sleep(impulse_delay)
            self.pin_b.drive_high()
            time.sleep(impulse_delay)
            self.pin_a.drive_low()
            time.sleep(impulse_delay)
            self.pin_b.drive_low()
            time.sleep(impulse_delay)

    def test_can_provides_correct_position(self):
        encoder = Encoder(self.settings)
        expected_position = 40
        self._send_cnt(expected_position, 0.02)
        position = encoder.position
        self.assertEqual(expected_position, position)
    
    def test_can_provides_correct_speed(self):
        encoder = Encoder(self.settings)
        current_time = time.time()
        velocity = None
        cnt = 0
        delta_time = 0
        possible_error = 1
        
        while True:
             
            if time.time() - current_time > 1:
                velocity = encoder.velocity
                delta_time = time.time() - current_time
                break
            self._send_cnt(1,0.025)
            cnt +=1

        expected_velocity = cnt/delta_time

        print(f"{expected_velocity=}, {possible_error=}, {velocity=}")

        self.assertTrue(expected_velocity - possible_error <= velocity <= expected_velocity + possible_error)

    def test_can_provides_correct_direction(self):
        self.assertTrue(True)
    
    def test_can_handle_wrong_types(self):
        self.assertTrue(True)
    

if __name__ == '__main__':
    unittest.main()
