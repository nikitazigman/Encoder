from typing import Union

if __package__:
    from .encoder import EncoderData, Encoder, EncoderInterface
    from .fabrics import range_converter_fabric, value_converter_fabric, RangeType, ValueType
else:
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
    
    def set_range_type(self, range_type: Union[RangeType, int]):
        self.range_type = RangeType(range_type)
    
    def set_value_type(self, value_type: Union[ValueType, int]):
        self.value_type = ValueType(value_type)
    
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