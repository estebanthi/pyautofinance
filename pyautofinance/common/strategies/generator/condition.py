class Condition:

    def __init__(self, line1, comparison, line2):
        self.line1 = line1
        self.comparison = comparison
        self.line2 = line2

    def __repr__(self):
        return f"{self.line1} {self.comparison} {self.line2}"

    def __eq__(self, other):
        return self.line1 == other.line1 and self.comparison == other.comparison and self.line2 == other.line2

    def is_compatible(self, other):
        if self.line1 == other.line1 and self.line2 == other.line2:
            if self.comparison == '>' and other.comparison == '<=':
                return False
            if self.comparison == '<' and other.comparison == '>=':
                return False
            if self.comparison == '>=' and other.comparison == '<':
                return False
            if self.comparison == '<=' and other.comparison == '>':
                return False
            if self.comparison == '=' and other.comparison == '!=':
                return False
            if self.comparison == '!=' and other.comparison == '=':
                return False
        if self == other:
            return False
        return True

    def __hash__(self):
        return hash(self.line1) + hash(self.comparison) + hash(self.line2)

    def get_indicators(self):
        return [self.line1.get_indicator(), self.line2.get_indicator()]
