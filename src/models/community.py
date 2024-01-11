from typing import Generator

import networkx as nx

import numpy as np

from src.models import Actor, Channel


class Community:
    """
    Base class representing a community
    nvars and w depend on each other
    """

    def __init__(self, network_size, nvars):
        net = nx.complete_graph(network_size)
        print(net)
        self._net = net
        self.nvars = nvars
        self.size = network_size
        self._channels_built = False

        # set default parameters of community actors
        for node, data in net.nodes(data=True):
            actor = Actor(node, data)
            data['actor'] = actor

    def init_channels(self):
        """
        Configures channels between actors, based on actor's confidence and dialog chance.
        Must be called after all actor configs.
        Not perfect, need to fine a more elegant way to do it.
        """
        self._channels_built = True
        # set parameters of community channels
        for a, b, data in self._net.edges(data=True):
            channel = Channel(self.actor(a), self.actor(b), data)
            p, q = channel.actor1.confidence_level, channel.actor2.confidence_level
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



