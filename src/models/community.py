from typing import Generator

import networkx as nx

import numpy as np

from src.models import Actor, Channel, Observation
from src.utils import preference, bernoulli


class Community:
    """
    Base class representing a community
    nvars and w depend on each other
    """

    def __init__(self, network_size, nvars, rho=20, low_confidence=0.2, high_confidence=0.6, dialog_chance=1.0):
        rg = np.random.default_rng()
        net = nx.complete_graph(network_size)
        print(net)
        self._net = net
        self.nvars = nvars
        self.size = network_size
        self._channels_built = False

        # set default parameters of community actors
        for node, data in net.nodes(data=True):
            actor = Actor(node, data, nvars)
            actor.rho = rho
            actor.confidence = rg.uniform(low=low_confidence, high=high_confidence)
            actor.dialog_chance = dialog_chance
            actor.uncertain_preference()
            data['actor'] = actor

    def build_channels(self):
        """
        Configures channels between actors, based on actor's confidence and dialog chance.
        Must be called after all actor configs.
        Not perfect, need to fine a more elegant way to do it.
        """
        self._channels_built = True
        # set parameters of community channels
        for a, b, data in self._net.edges(data=True):
            channel = Channel(self.actor(a), self.actor(b), data)
            p, q = channel.actor1.confidence, channel.actor2.confidence
            channel.dialog_matrix = np.array([p, 1 - p, 1 - q, q], float).reshape(2, 2)
            data['channel'] = channel
            channel.activation = channel.actor1.dialog_chance

    def actors(self) -> Generator[Actor, None, None]:
        for node, data in self._net.nodes(data=True):
            yield data['actor']

    def actor(self, node) -> Actor:
        return self._net.nodes[node]['actor']

    def channels(self) -> Generator[Channel, None, None]:
        assert self._channels_built, "Community.setup_channels() was not called"
        for a, b, data in self._net.edges(data=True):
            yield data['channel']

    def channel(self, edge):
        assert self._channels_built, "Community.setup_channels() was not called"
        return self._net.edges[edge]['channel']

    def poll(self) -> Observation:
        # polling simulation

        # It def belongs here as it's actually a "poll", hence there's some probability of different answers
        # based on preference density.
        disclaimers = 0
        choices = np.zeros(self.nvars)

        for actor in self.actors():
            hn = preference.normalized_entropy(actor.preference)
            if bernoulli.trial(np.power(hn, actor.rho)):
                disclaimers += 1  # actor 'n' disclaims a choice
            else:
                # actor 'n' chooses
                choice = np.random.choice(self.nvars, p=actor.preference)
                choices[choice] += 1

        # compute average preference density
        W = np.zeros(self.nvars)
        for actor in self.actors():
            np.add(W, actor.preference, W)
        np.multiply(W, 1.0 / self.size, W)

        if disclaimers == self.size:  # all actors disclaimed their choice
            return Observation(W, 1.0, preference.uncertainty(self.nvars))

        nondisclaimers = self.size - disclaimers
        np.multiply(choices, 1.0 / nondisclaimers, choices)

        return Observation(W, disclaimers / self.size, choices)

