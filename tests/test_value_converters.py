import math
import unittest

from value_converter import ValueConveterInterface
from fabrics import value_converter_fabric, ValueType
                            

class TestValueConverter(unittest.TestCase):
    def test_degree_converter(self):
        value = 30
        period  = 100
        expected_degree = (30 / 100) * 360
        DegreeConverter = value_converter_fabric(ValueType.degree)
        degree_converter:ValueConveterInterface = DegreeConverter()
        degree = degree_converter.convert(value, period) 
        self.assertEqual(degree, expected_degree)

    def test_degree_wrong_values_period_less_value(self):
        value = 100
        period  = 30

        DegreeConverter = value_converter_fabric(ValueType.degree)
        degree_converter = DegreeConverter()
        
        with self.assertRaises(ValueError):
            degree_converter.convert(value, period) 
            
    def test_degree_wrong_value_type(self):
        value = "10"
        period  = 30

        DegreeConverter = value_converter_fabric(ValueType.degree)
        degree_converter:ValueConveterInterface = DegreeConverter()
        
        with self.assertRaises(TypeError):
            degree_converter.convert(value, period) 
        
    def test_radian_converter(self):
        value = 30
        period  = 100
        expected_radian = (30 / 100) * 360 * (math.pi/180)
        DegreeConverter = value_converter_fabric(ValueType.radians)
        degree_converter = DegreeConverter()
        radian = degree_converter.convert(value, period) 
        self.assertEqual(radian, expected_radian)

    def test_radian_wrong_values_period_less_value(self):
        value = 100
        period  = 30

        RadianConverter = value_converter_fabric(ValueType.radians)
        radian_converter = RadianConverter()
        
        with self.assertRaises(ValueError):
            radian_converter.convert(value, period) 
        
    
    def test_radian_wrong_value_type(self):
        value = '10'
        period  = 30

        RadianConverter = value_converter_fabric(ValueType.radians)
        radian_converter = RadianConverter()
        
        with self.assertRaises(TypeError):
            radian_converter.convert(value, period) 


if __name__ == '__main__':
    unittest.main()