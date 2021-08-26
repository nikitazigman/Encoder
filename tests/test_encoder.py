import math
from os import WTERMSIG
import time
import unittest
from unittest.mock import patch, call

from gpiozero.pins.mock import MockFactory, MockPin

from encoder import Encoder, EncoderData
from fabrics import ValueType, RangeType, value_converter_fabric, range_converter_fabric


class TestEncoder(unittest.TestCase):

    def setUp(self):
        settings = {
            "range_converter": range_converter_fabric(RangeType.zero_to_period),
            "value_converter": value_converter_fabric(ValueType.degree),
            "pin_a": 20,            
            "pin_b": 21,
            "duration": 0.1, # 100 ms
            "period": 360,
            "virtual": True,
        }
        self.settings = EncoderData(**settings)
        self.mock_facktory = MockFactory()
        self.pin_a: MockPin = self.mock_facktory.pin(20)
        self.pin_b: MockPin = self.mock_facktory.pin(21)

        self.impulse_delay = 0.02 # sec

    def tearDown(self):
        self.mock_facktory.close()
        self.pin_a.close()
        self.pin_a.close()

    def _send_cnt(self, cnt_number: int, impulse_delay: float):
        for i in range(cnt_number):
            self.pin_a.drive_high()
            time.sleep(impulse_delay)
            self.pin_b.drive_high()
            time.sleep(impulse_delay)
            self.pin_a.drive_low()
            time.sleep(impulse_delay)
            self.pin_b.drive_low()
            time.sleep(impulse_delay)
   
    def test_can_provides_correct_position_speed_direction(self):
        encoder = Encoder(self.settings)
        cnt = 70

        self._send_cnt(cnt, 0.0025)

        self.assertEqual(cnt, encoder.position)

    
    def test_can_handle_wrong_types(self):
        wrong_settings_type = dict()

        with self.assertRaises(TypeError):
            Encoder(wrong_settings_type)
    

if __name__ == '__main__':
    unittest.main()

