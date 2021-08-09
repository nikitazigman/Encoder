import unittest

from  pydantic import ValidationError

from builder import EncoderBuilder
from encoder import Encoder
from range_converter import MinusHalfToHAlfRange, ZeroToPeriodRange
from value_converter import DegreeConverter, RadianConverter

class TestBuilder(unittest.TestCase):
    def setUp(self):
        settings = {
            "pin_a": 20,            
            "pin_b": 21,
            "duration": 0.1, # 100 ms
            "period": 360,
        }

    def test_default_settings(self):
        builder = EncoderBuilder(**self.settings)
        encoder: Encoder = builder.get_encoder()

        self.assertEqual(encoder._pin_a, self.settings['pin_a'])
        self.assertEqual(encoder._pin_b, self.settings['pin_b'])
        self.assertEqual(encoder._duration, self.settings['duration'])
        self.assertEqual(encoder._period_cnt, self.settings['period'])

        self.assertEqual(type(encoder._range_converter), type(ZeroToPeriodRange()))
        self.assertEqual(type(encoder._value_converter), type(DegreeConverter()))

    def test_wrong_settings(self):
        self.settings['pin_a'] = 1.5
        builder = EncoderBuilder(**self.settings)

        with self.assertRaises(ValidationError):
            builder.get_encoder()

    def test_can_choose_value_type(self):
        builder = EncoderBuilder(**self.settings)
        builder.set_value_type_radians()

        encoder: Encoder = builder.get_encoder()
        
        self.assertEqual(type(encoder._value_converter), type(DegreeConverter()))


    def test_can_choose_range_type(self):
        builder = EncoderBuilder(**self.settings)
        builder.set_range_type_half_to_half()
        
        encoder: Encoder = builder.get_encoder()

        self.assertEqual(type(encoder._range_converter), type(MinusHalfToHAlfRange()))

