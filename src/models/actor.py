import array
import numpy as np

from src.models import HashWrapper
from src.utils import bernoulli, preference


class Actor(HashWrapper):
    """
    Decorator over a networkx graph node
    """
    def __init__(self, node: int, data, nvars: int):
        super().__init__(data)
        self.node = node
        self._nvars = nvars

    @property
    def rho(self):
        return self._data['rho']

    @rho.setter
    def rho(self, value):
        self._data['rho'] = value

    @property
    def confidence(self):
        """
        Probability that actor will preserve their choice.
        """
        return self._get('confidence')

    @confidence.setter
    def confidence(self, value: float):
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
    def preference(self) -> array:
        """
        Actor's preference density. Array size corresponds to the nvars.
        Represented as 'w' in the article
        """
        return self._get('w')

    @preference.setter
    def preference(self, value: array):
        self._set('w', value)

    def uncertain_preference(self):
        self.preference = preference.uncertainty(self._nvars)

    def strong_preference(self, choice):
        self.preference = np.zeros(self._nvars)
        self.preference[choice] = 1.0
