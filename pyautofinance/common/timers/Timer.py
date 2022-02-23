from abc import ABC, abstractmethod


class Timer(ABC):

    def __init__(self, name, **kwargs):
        self.name = name
        self.parameters = kwargs

    @abstractmethod
    def get_function(self):  # Returns the function of the timer
        pass
