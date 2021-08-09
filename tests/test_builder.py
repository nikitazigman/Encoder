import unittest

from pydantic import ValidationError

from builder import EncoderBuilder
from encoder import Encoder
from range_converter import MinusHalfToHAlfRange, ZeroToPeriodRange
from value_converter import DegreeConverter, RadianConverter

class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.settings = {
            "pin_a": 20,            
            "pin_b": 21,
            "duration": 0.1, # 100 ms
            "period": 360,
        }

    def test_default_settings(self):
        builder = EncoderBuilder(**self.settings)
        builder._test = True
        
        builder.get_encoder()
        settings = builder.get_encoder_settings()

        self.assertEqual(settings['pin_a'], self.settings['pin_a'])
        self.assertEqual(settings['pin_b'], self.settings['pin_b'])
        self.assertEqual(settings['duration'], self.settings['duration'])
        self.assertEqual(settings['period'], self.settings['period'])

        self.assertTrue('ZeroToPeriodRange' in str(settings["range_converter"]))
        self.assertTrue('DegreeConverter' in str(settings["value_converter"]))

    def test_wrong_settings(self):
        self.settings['pin_a'] = "asd"
        builder = EncoderBuilder(**self.settings)
        builder._test = True

        with self.assertRaises(ValidationError):
            builder.get_encoder()

    def test_can_choose_value_type(self):
        builder = EncoderBuilder(**self.settings)
        builder.set_value_type_radians()
        builder._test = True

        builder.get_encoder()
        settings = builder.get_encoder_settings()
        self.assertTrue('RadianConverter' in str(settings["value_converter"]))


    def test_can_choose_range_type(self):
        builder = EncoderBuilder(**self.settings)
        builder.set_range_type_half_to_half()
        builder._test = True

        builder.get_encoder()
        settings = builder.get_encoder_settings()

        self.assertTrue('MinusHalfToHAlfRange' in str(settings["range_converter"]))

