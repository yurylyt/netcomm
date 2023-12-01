import networkx as nx

from wrappers import Actor, Channel
from utils import *


class Community:
    """
    Base class representing a community
    """
    def __init__(self, network_size, nvars=2, rho=20):
        rg = np.random.default_rng()
        net = nx.complete_graph(network_size)
        print(net)
        self._net = net
        self.nvars = nvars
        self.size = network_size

        # set parameters of community actors
        for node, data in net.nodes(data=True):
            actor = Actor(node, data)
            actor.rho = rho
            actor.choice = 0 if actor.node == 0 else DISCLAIMER
            data['actor'] = Actor(node, data)

        # set parameters of community channels
        for a, b, data in net.edges(data=True):
            channel = Channel(a, b, data)
            data['channel'] = channel

            alice = channel.actor1
            if alice == 0:
                channel.a = 1.0
                channel.D = define_dialogue_matrix(1.0, rg.uniform(low=0.2, high=0.6))
            else:
                channel.a = 1.0
                channel.D = define_dialogue_matrix(rg.uniform(low=0.2, high=0.6), rg.uniform(low=0.2, high=0.6))

        self._init_preference()

    def _init_preference(self):
        print("Specifying the experiment...")
        # specify initial prefernce densities of community actors
        for actor in self.actors():
            if actor.node == 0:
                actor.w = np.array([1.0, 0.0], float)
            elif actor.node == 1:
                actor.w = np.array([0.0, 1.0], float)
            else:
                actor.w = uncertainty(self.nvars)

    def actors(self):
        for node, data in self._net.nodes(data=True):
            yield data['actor']

    def actor(self, node):
        return self._net.nodes[node]['actor']

    def channels(self):
        for a, b, data in self._net.edges(data=True):
            yield data['channel']

    def channel(self, edge):
        return self._net.edges[edge]['channel']


