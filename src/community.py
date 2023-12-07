from typing import Generator

import networkx as nx

from wrappers import Actor, Channel
from utils import *


class Community:
    """
    Base class representing a community
    nvars and w depend on each other
    """

    def __init__(self, network_size, nvars=2, rho=20):
        rg = np.random.default_rng()
        net = nx.complete_graph(network_size)
        print(net)
        self._net = net
        self.nvars = nvars
        self.size = network_size

        # set default parameters of community actors
        for node, data in net.nodes(data=True):
            actor = Actor(node, data)
            actor.rho = rho
            actor.choice = DISCLAIMER
            actor.confidence = rg.uniform(low=0.2, high=0.6)
            actor.dialog_chance = 1.0
            actor.preference = uncertainty(self.nvars)
            data['actor'] = Actor(node, data)

        # define a leader
        alice = self.actor(0)
        alice.choice = 0
        alice.confidence = 1.0
        alice.dialog_chance = 1.0
        alice.preference = np.array([1.0, 0.0], float)

        # define another leader
        bob = self.actor(1)
        bob.preference = np.array([0.0, 1.0], float)

        # set parameters of community channels
        for a, b, data in net.edges(data=True):
            channel = Channel(self.actor(a), self.actor(b), data)
            channel.dialog_matrix = define_dialogue_matrix(channel.actor1.confidence, channel.actor2.confidence)
            data['channel'] = channel
            channel.activation = channel.actor1.dialog_chance

    def actors(self) -> Generator[Actor, None, None]:
        for node, data in self._net.nodes(data=True):
            yield data['actor']

    def actor(self, node) -> Actor:
        return self._net.nodes[node]['actor']

    def channels(self) -> Generator[Channel, None, None]:
        for a, b, data in self._net.edges(data=True):
            yield data['channel']

    def channel(self, edge):
        return self._net.edges[edge]['channel']


