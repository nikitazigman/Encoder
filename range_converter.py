from abc import ABC, abstractmethod


class RangeConverterInterface(ABC):
    """abstract interface to RangeConverters Classes"""
    
    def convert_range(self, value: int, period: int) -> int:
        """it gives value and period and return converted to the range-type position """

        if not type(value) is type(period) and type(period) is int:
            raise TypeError("value and period have to have type int")
        
        if period == 0:
            raise ZeroDivisionError("period can't be equal 0")

        return value % period
        

class MinusHalfToHAlfRange(RangeConverterInterface):
    def convert_range(self, value: int, period: int) -> int:
        value = super().convert_range(value, period)
        
        half_period = period / 2
        if value > half_period:
            value = value - period
        elif value < -half_period:
            value = period - value
        return value

class ZeroToPeriodRange(RangeConverterInterface):

    def convert_range(self, value: int, period: int) -> int:
        value = super().convert_range(value, period)

        if value > period:
            value = 0
        elif value < 0:
            value = period

        return value

