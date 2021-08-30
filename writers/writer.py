import abc

class Writer(abc.ABC):
    @abc.abstractclassmethod
    def write(self, steering, throttle, frame):
        pass