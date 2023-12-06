from community import Community
from utils import *
from dataclasses import dataclass


class Protocol:
    """
    Community observation protocol
    """

    def __init__(self, community: Community):
        self._community = community
        self._protocol = []
        self.observe()

    def observe(self):
        self._protocol.append(self._observe())

    def _observe(self):
        # polling simulation
        netcomm = self._community
        for actor in netcomm.actors():
            hn = h(actor.w)
            if bernoulli_trial(np.power(hn, actor.rho)):
                # actor 'n' disclaims a choice
                actor.choice = DISCLAIMER
            else:
                # actor 'n' chooses
                actor.choice = np.random.choice(netcomm.nvars, p=actor.w)
        # compute average preference density
        W = np.zeros(netcomm.nvars)
        for actor in netcomm.actors():
            np.add(W, actor.w, W)
        number_of_nodes = netcomm.size
        np.multiply(W, 1.0 / number_of_nodes, W)
        # compute polling result
        DP = len([1 for a in netcomm.actors() if a.choice == DISCLAIMER])
        if DP == number_of_nodes:
            # all community actors disclaimed a choice
            return W, 1.0, uncertainty(netcomm.nvars)
        NP = number_of_nodes - DP
        WP = netcomm.nvars * [None]
        for v in range(netcomm.nvars):
            WP[v] = len([1 for a in netcomm.actors() if a.choice == v])
            WP[v] /= NP
        DP /= number_of_nodes
        return self.ProtocolEntry(W, DP, WP)

    def data(self):
        return self._protocol

    @dataclass
    class ProtocolEntry:
        W: list
        DP: float
        WP: list

