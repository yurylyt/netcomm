import array
import numpy as np

from src.models import HashWrapper
from src.utils import preference


class Actor(HashWrapper):
    """
    Decorator over a networkx graph node
    """
    def __init__(self, node: int, data):
        super().__init__(data)
        self.node = node

    @property
    def rho(self):
        return self._data['rho']

    @rho.setter
    def rho(self, value):
        self._data['rho'] = value

    @property
    def confidence_level(self):
        """
        Probability that actor will preserve their choice.
        """
        return self._get('confidence')

    @confidence_level.setter
    def confidence_level(self, value: float):
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

    def is_uncertain(self, nvars):
        self.preference = preference.uncertainty(nvars)

    def chooses(self, choice):
        self.preference = np.zeros(len(self.preference))
        self.preference[choice] = 1.0
