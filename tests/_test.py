import threading 
import time 

 
class Speed(threading.Thread):
    def __init__(self, encoder):
        super().__init__()
        self._encoder = encoder
        self.status = True

    def run(self):
        while self.status:
            print(f"{self._encoder.position=}")
            self._encoder._speed += 2 
            time.sleep(1)


class Encoder:
    def __init__(self):
        self._position = 0
        self._speed = 0

    @property
    def position(self):
        self._position += 1
        return self._position
    
    @property
    def velocity(self):
        return self._speed
    

class EncoderInt:
    def __init__(self):
        self.encoder = Encoder()
        self.speed = Speed(self.encoder)
    
    def get_position(self):
        return self.encoder.position
    
    def get_velocity(self):
        return self.encoder.velocity
    
    def __del__(self):
        print('destructor was')
        self.speed.status=False


if __name__ == '__main__':
    encoder = EncoderInt()
    for _ in range(3):
        time.sleep(1)
        print(f"{encoder.get_position()=}")
        print(f"{encoder.get_velocity()=}")

