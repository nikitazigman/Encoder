import unittest

from fabrics import *
from range_converter import *
from value_converter import *



class TestFabric(unittest.TestCase):
    def test_range_fabric_correct_return(self):
        converters = {
            RangeType.minus_half_to_half: MinusHalfToHAlfRange,
            RangeType.zero_to_period: ZeroToPeriodRange,
        }
        
        for range_type in RangeType:
            converter_interface = range_converter_fabric(range_type)
            self.assertEqual(type(converters[range_type]), type(converter_interface))

    def test_range_fabric_wrong_type(self):
        range_type = 1

        with self.assertRaises(TypeError):
            range_converter_fabric(range_type)

    def test_value_fabric_correct_return(self):
        converters = {
            ValueType.degree: DegreeConverter,
            ValueType.radians: RadianConverter,
        }
        
        for value_type in ValueType:
            converter_interface = value_converter_fabric(value_type)
            self.assertEqual(type(converters[value_type]), type(converter_interface))

    def test_value_fabric_wrong_type(self):
        range_type = 1

        with self.assertRaises(TypeError):
            value_converter_fabric(range_type)


if __name__ == '__main__':
    unittest.main()