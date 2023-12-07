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
    def __init__(self, node: int, data):
        super().__init__(data)
        self.node = node
        self.result_list = []

    @property
    def rho(self):
        return self._data['rho']

    @rho.setter
    def rho(self, value):
        self._data['rho'] = value

    @property
    def choice(self):
        """
        actor's current choice. Should be moved as a local variable to Observer.
        However, need to consider the initial choice for 'alice' aka leader
        :return:
        """
        return self._get('choice')

    @choice.setter
    def choice(self, value):
        self._set('choice', value)

    @property
    def confidence(self):
        """
        Probability that actor will preserve their choice.
        """
        return self._get('confidence')

    @confidence.setter
    def confidence(self, value):
        self._set('confidence', value)

    @property
    def dialog_chance(self):
        """
        Probability that actor will engage in a dialog.
        <br/>
        Defines channel activation probability if the actor is the first in a channel actors pair
        """
        return self._get('dialog_chance')

    @dialog_chance.setter
    def dialog_chance(self, value):
        self._set('dialog_chance', value)

    @property
    def result_list(self):
        return self._data['result_list']

    @result_list.setter
    def result_list(self, value):
        self._data['result_list'] = value

    @property
    def preference(self) -> array:
        """
        Actor's preference density. Array size corresponds to the nvars.
        Represented as 'w' in the article
        """
        return self._get('w')

    @preference.setter
    def preference(self, value: array):
        self._set('w', value)

class Channel(HashWrapper):
    """
    Decorator for a networkx graph edge. Syntax sugar really
    """
    def __init__(self, actor1: Actor, actor2: Actor, data):
        super().__init__(data)
        self.actor1 = actor1
        self.actor2 = actor2

    def is_active(self):
        return bernoulli_trial(self.activation)

    @property
    def dialog_matrix(self):
        """
        Channel's dialog matrix. Represented as D in the article
        """
        return self._get('D')

    @dialog_matrix.setter
    def dialog_matrix(self, value):
        self._set('D', value)

    @property
    def activation(self):
        """
        Channel activation probability.
        """
        return self._get('a')

    @activation.setter
    def activation(self, value):
        self._set('a', value)
