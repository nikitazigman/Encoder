# Encoder

Here is Python Encoder lib which extends RotaryEncoder class of gpiozero

## How to use: 

``` python
from builder import EncoderBuilder
from encoder import EncoderInterfacec
from fabrics import RangeType, ValueTypes

settings = {
    "pin_a": 20,            
    "pin_b": 21,
    "period": 360,
}


if __name__ == "__main__":
    builder = EncoderBuilder(**settings)
    builder.set_value_type(ValueTypes.minus_half_to_half) # defult zero_to_period
    builder.set_range_type(RangeType.radians) # default degree
    # or 
    # builder.set_value_type(2)
    # builder.set_range_type(2)

    encoder: EncoderInterface = builder.get_encoder()
    
    while True:
        print(f"{encoder.position=}")

```