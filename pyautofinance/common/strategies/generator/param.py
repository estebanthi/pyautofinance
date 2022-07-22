from abc import ABC, abstractmethod
import random


class Param(ABC):

    def __init__(self, name, possible_values, value=None):
        self.name = name
        self.possible_values = possible_values
        self.value = value

    def generate(self):
        self.value = random.choice(self.possible_values)

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

    def __repr__(self):
        return f"{self.name} : {self.value}"

    def __hash__(self):
        return hash(self.name) + hash(self.value)