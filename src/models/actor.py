import array
import numpy as np

from models import HashWrapper
from utils import preference, bernoulli


class Actor(HashWrapper):
    """
    Decorator over a networkx graph node
    """
    def __init__(self, node: int, data):
        super().__init__(data)
        self.node = node

    @property
    def decisiveness(self):
        return self._data['decisiveness']

    @decisiveness.setter
    def decisiveness(self, value):
        self._data['decisiveness'] = value

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

    def make_decision(self):
        # normalized entropy indicates how different values are in actor.preference.
        # Similar/close values produce higher entropy value.
        # The higher value is, the higher chances for the disclaimer.
        # if actor's uncertain (i.e. preference values are the same),
        # then entropy value is 1.0, meaning it will disclaim for sure
        hn = preference.normalized_entropy(self.preference)

        # rho seems to be used to make the curve steeper for entropy,
        # making it very close to 0 for almost half of lower values
        # And then rising very fast
        rho = np.exp(self.decisiveness)
        if bernoulli.trial(np.power(hn, rho)):
            return preference.DISCLAIMER

        return np.random.choice(len(self.preference), p=self.preference)


