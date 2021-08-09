from encoder import EncoderData, Encoder, EncoderInterface
from fabrics import range_converter_fabric, value_converter_fabric, RangeType, ValueType


class EncoderBuilder:
    """It encapsulate the flow of building the encoder"""
    
    def __init__(self, pin_a: int, pin_b: int, duration: float, period:int):
        self.settings = {
            "pin_a": pin_a,            
            "pin_b": pin_b,
            "duration": duration, # ms
            "period": period,
        }
        self._test = False

        self.range_type = RangeType.zero_to_period
        self.value_type = ValueType.degree
    
    def set_range_type_zero_to_period(self):
        self.range_type = RangeType.zero_to_period
    
    def set_range_type_half_to_half(self):
        self.range_type = RangeType.minus_half_to_half

    def set_value_type_degree(self):
        self.value_type = ValueType.degree
    
    def set_value_type_radians(self):
        self.value_type = ValueType.radians
    
    def set_virtual(self):
        self.settings["virtual"] = True
    
    def get_encoder(self) -> EncoderInterface:
        self.settings["range_converter"] = range_converter_fabric(self.range_type)
        self.settings["value_converter"] = value_converter_fabric(self.value_type)
        self.encoder_data = EncoderData(**self.settings)
        
        if not self._test:
            print(self._test)
            return Encoder(self.encoder_data)

    def get_encoder_settings(self) -> dict:
        return self.encoder_data.dict()