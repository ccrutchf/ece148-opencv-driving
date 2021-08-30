import abc

class Driver(abc.ABC):
    @abc.abstractmethod
    def get_controls(self):
        pass