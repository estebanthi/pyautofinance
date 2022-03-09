

class ComponentsAssembly:

    def __init__(self, broker, strategy, datafeed, sizer, metrics_collection, *args):
        self._components = [broker, strategy, datafeed, sizer, metrics_collection, list(args)]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self._components):
            component = self._components[self.index]
            self.index += 1
            return component

        raise StopIteration