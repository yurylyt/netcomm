import array

from utils import bernoulli_trial


class HashWrapper:
    """
    Uses explicit property definition instead of __getattr__/__setattr__ approach for performance reasons

    """
    def __init__(self, data):
        self._data = data

    def _get(self, item):
        return self._data[item]

    def _set(self, key, value):
        self._data[key] = value


class Actor(HashWrapper):
    """
    Decorator over a networkx graph node
    """
    def __init__(self, node, data):
        super().__init__(data)
        self.node = node

    @property
    def rho(self):
        return self._data['rho']

    @rho.setter
    def rho(self, value):
        self._data['rho'] = value

    @property
    def choice(self):
        """
        actor's current choice. SHould be moved as a local variable to Observer.
        However, need to consider the initial choice (
        :return:
        """
        return self._get('choice')

    @choice.setter
    def choice(self, value):
        self._set('choice', value)


    @property
    def result_list(self):
        return self._data['result_list']

    @result_list.setter
    def result_list(self, value):
        self._data['result_list'] = value

    @property
    def w(self) -> array:
        """
        Actor's preference density. Array size corresponds to the nvars
        """
        return self._get('w')

    @w.setter
    def w(self, value: array):
        self._set('w', value)

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

    @property
    def D(self):
        """
        :return: channel's dialog matrix
        """
        return self._get('D')

    @D.setter
    def D(self, value):
        self._set('D', value)

    @property
    def a(self):
        """
        :return: channel activation probability
        """
        return self._get('a')

    @a.setter
    def a(self, value):
        self._set('a', value)