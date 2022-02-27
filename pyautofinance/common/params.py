class ParamsCollection:

    def __init__(self, params_list):
        self.params_list = params_list

    def __getitem__(self, item):
        return self.params_list[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.params_list):
            param = self.params_list[self.index]
            self.index += 1
            return param
        else:
            raise StopIteration
