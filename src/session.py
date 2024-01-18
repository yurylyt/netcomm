import numpy as np

from src.models import Channel
from src.models.community import Community


class Session:
    def __init__(self, community: Community):
        self._community = community
        self._results = [[] for _ in range(community.size)]

    def simulate(self):

        # simulate session dialogues
        for channel in self._community.channels():
            self._activate_channel(channel)

        # compute the previous session result for each community actor
        self._compute_results()

    def _activate_channel(self, channel: Channel):
        if channel.is_active():
            # determine actors participating as Alice and Bob in the current dialogue
            alice, bob = channel.actor1, channel.actor2
            # ------------------------------------------------------
            wA, wB = self._simulate_dialog(channel.dialog_matrix, alice.preference, bob.preference)
            self._results[alice.node].append(wA)
            self._results[bob.node].append(wB)

    def _compute_results(self):
        for i, actor in enumerate(self._community.actors()):
            result_list = self._results[i]
            if result_list:
                # actor 'n' participates at least in one dialogue
                ndialogues = len(result_list)
                w = np.zeros(self._community.nvars)
                for wc in result_list:
                    np.add(w, wc, w)
                np.multiply(w, 1.0 / ndialogues, actor.preferences)


    def _simulate_dialog(self, D, wA, wB):
        # get dialogue matrix of the current dialogue and
        # the preference densities of its participants
        nvars = self._community.nvars
        wA_result = np.zeros(nvars)
        wB_result = np.zeros(nvars)
        for v in range(nvars):
            wA_result[v] = D[0, 0] * wA[v] + D[0, 1] * wB[v]
            wB_result[v] = D[1, 0] * wA[v] + D[1, 1] * wB[v]
        return wA_result, wB_result






