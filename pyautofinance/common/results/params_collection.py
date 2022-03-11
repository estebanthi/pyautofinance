class ParamsCollection:

    def __init__(self, params_list):
        self.params_list = params_list

    def __getitem__(self, item):
        return self.params_list[item]

    def __iter__(self):
        for key, value in self.params_list:
            yield key, value

    def __repr__(self):
        params_list = []
        for param in self.params_list:
            params_list.append(str(param))
        return ' '.join(params_list)
