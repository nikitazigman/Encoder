import math

from abc import ABC, abstractmethod


class ValueConveterInterface(ABC):
    """abstract interface to ValueConverters Classes"""

    @abstractmethod
    def convert(self, position: int, period: int) -> float:
        """ method convert value to other measurement range e.g degree, radians etc."""

        if period < position:
            raise ValueError("position can't be bigger than period")
        
        if not type(period) is type(position) and type(position) is int:
            raise TypeError("position and period have to have type int")
                

class DegreeConverter(ValueConveterInterface):
    def convert(self, position: int, period: int) -> float:
        super().convert(position, period)

        return (position / period) * 360


class RadianConverter(DegreeConverter):
    MULTIPLIER_DEGREE_TO_RADIAN_VALUE = math.pi / 180

    def convert(self, position: int, period: int) -> float:
        return super().convert(position, period) * self.MULTIPLIER_DEGREE_TO_RADIAN_VALUE

