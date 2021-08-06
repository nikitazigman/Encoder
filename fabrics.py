from enum import  Enum

from value_converter import (DegreeConverter, 
                            RadianConverter,
                            ValueConveterInterface)
from range_converter import (RangeConverterInterface, 
                            MinusHalfToHAlfRange,
                            ZeroToPeriodRange)

#ToDo think about builder

class RangeType(Enum):
    minus_half_to_half = 1
    zero_to_period = 2


class ValueType(Enum):
    degree = 1
    radians = 2

def range_converter_fabric(range_type: RangeType) -> RangeConverterInterface:
    """here is a fabric for range converters it returns convert class depends on range_type"""
    
    if type(range_type) is not RangeType:
        raise TypeError('range_type has to have RangeType type')
    
    else:
        classes = {
            RangeType.minus_half_to_half: MinusHalfToHAlfRange,
            RangeType.zero_to_period: ZeroToPeriodRange,
        }

        return classes[range_type]


def value_converter_fabric(value_type: ValueType) -> ValueConveterInterface:
    """here is a fabric for range converters it returns convert class depends on range_type"""
    
    if type(value_type) is not ValueType:
        raise TypeError('value_type has to have ValueType type')
    
    else:
    
        classes = {
            value_type.degree: DegreeConverter,
            value_type.radians: RadianConverter,
        }

        return classes[value_type]