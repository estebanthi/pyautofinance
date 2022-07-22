from abc import ABC, abstractmethod


class Line(ABC):
    parent = None
    mapping = ''
    type = None

    def __init__(self, params=[]):
        self.params = params

    def __eq__(self, other):
        return self.parent == other.parent and self.mapping == other.mapping and self.type == other.type and self.params == other.params

    def __hash__(self):
        return hash(self.parent) + hash(self.mapping) + hash(self.type) + hash(sum([hash(param) for param in self.params]))

    def __repr__(self):
        return f"Name : {self.mapping} | Params : {self.params}"

    def generate_params(self):
        for param in self.params:
            param.generate()

    def get_indicator(self):
        return self.parent, self.params
