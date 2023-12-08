

from src.models import HashWrapper, Actor
from src.utils import bernoulli


class Channel(HashWrapper):
    """
    Decorator for a networkx graph edge. Syntax sugar really
    """
    def __init__(self, actor1: Actor, actor2: Actor, data):
        super().__init__(data)
        self.actor1 = actor1
        self.actor2 = actor2
        # TODO: move dialog matrix definition here

    def is_active(self):
        return bernoulli.trial(self.activation)

    @property
    def dialog_matrix(self):
        """
        Channel's dialog matrix. Represented as D in the article.
        Does not depend on number of choices.
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


