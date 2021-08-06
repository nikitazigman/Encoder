import unittest

from range_converter import RangeConverterInterface
from fabrics import RangeType, range_converter_fabric


class TestRangeConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.tested_dict = [
            {'val': 270, 'period': 100},
            {'val': 230, 'period': 100},
            {'val': -270, 'period': 100},
            {'val': -230, 'period': 100},
            {'val': 50, 'period': 100},
            {'val': -50, 'period': 100},
            {'val': 0, 'period': 100},
        ]
        return super().setUp() 

    def test_half_range_converter(self):
        RangeConverter = range_converter_fabric(RangeType.minus_half_to_half)
        range_converter: RangeConverterInterface = RangeConverterInterface[RangeConverter()]

        for test in self.tested_dict:
            expected_position = (test['val'] % test['period'])
            
            if expected_position > test['period']/2:
                expected_position -= test['period'] 
            elif expected_position < -test['period']/2:
                expected_position = test['period'] - expected_position
                
            position = range_converter.convert_range(test['val'], test['period'])

            self.assertEqual(position, expected_position,msg=f"wrong result with {test} values")

    def test_half_range_wrong_values_type(self):
        RangeConverter = range_converter_fabric(RangeType.minus_half_to_half)
        range_converter: RangeConverterInterface = RangeConverter()

        with self.assertRaises(TypeError):
            range_converter.convert_range(123.3, 100)
    
    def test_half_range_zero_period(self):
        RangeConverter = range_converter_fabric(RangeType.minus_half_to_half)
        range_converter: RangeConverterInterface = RangeConverter()

        with self.assertRaises(ZeroDivisionError):
            range_converter.convert_range(123, 0)

    def test_full_range_converter(self):
        RangeConverter = range_converter_fabric(RangeType.zero_to_period)
        range_converter: RangeConverterInterface = RangeConverter()

        for test in self.tested_dict:
            expected_position = (test['val'] % test['period'])
            if expected_position < 0:
                expected_position = test['period'] - expected_position

            position = range_converter.convert_range(test['val'], test['period'])    

            self.assertEqual(position, expected_position, msg=f"wrong result with {test} values")

    def test_full_range_wrong_values_type(self):
        RangeConverter = range_converter_fabric(RangeType.zero_to_period)
        range_converter: RangeConverterInterface = RangeConverter()

        with self.assertRaises(TypeError):
            range_converter.convert_range(123.3, 100)

    def test_full_range_zero_period(self):
        RangeConverter = range_converter_fabric(RangeType.zero_to_period)
        range_converter: RangeConverterInterface = RangeConverter()

        with self.assertRaises(ZeroDivisionError):
            range_converter.convert_range(123, 0)

if __name__ == '__main__':
    unittest.main()