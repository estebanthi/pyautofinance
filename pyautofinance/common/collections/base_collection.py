class BaseCollection:

    def __init__(self, items=None):
        self.items = items
        if not items:
            self.items = []

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        try:
            item = self.items[self.index]
            self.index += 1
            return item
        except IndexError:
            raise StopIteration

    def __setitem__(self, key, value):
        self.items[key] = value

    def __repr__(self):
        return str(self.items)

    def __len__(self):
        return len(self.items)

    def append(self, item):
        self.items.append(item)

    def filter(self, method):
        return type(self)(list(filter(method, self)))

    def get_common_items(self, other):
        return list(set(self).intersection(set(other)))
