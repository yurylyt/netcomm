from utils import bernoulli_trial


class HashWrapper:
    def __init__(self, hash_obj):
        self._hash = hash_obj

    def __getattr__(self, item):
        return self._hash[item]

    def __setattr__(self, key, value):
        if key == "_hash":
            # This allows the initial dictionary to be set
            super().__setattr__(key, value)
        else:
            self._hash[key] = value


class Actor(HashWrapper):
    """
    Decorator over a networkx graph node
    """
    def __init__(self, node, data):
        super().__init__(data)
        self.node = node


class Channel(HashWrapper):
    """
    Decorator for a networkx graph edge. Syntax sugar really
    """
    def __init__(self, actor1, actor2, data):
        super().__init__(data)
        self.actor1 = actor1
        self.actor2 = actor2

    def is_active(self):
        return bernoulli_trial(self.a)
