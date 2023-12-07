import time
import numpy as np


class Session:
    """
    Session simulator
    """

    def __init__(self, community):
        self.community = community

    def _simulate_dialog(self, D, wA, wB):
        # clean auxiliary information
        nvars = self.community.nvars
        # get dialogue matrix of the current dialogue and
        # the preference densities of its participants
        wA_result = np.zeros(nvars)
        wB_result = np.zeros(nvars)
        for v in range(nvars):
            wA_result[v] = D[0, 0] * wA[v] + D[0, 1] * wB[v]
            wB_result[v] = D[1, 0] * wA[v] + D[1, 1] * wB[v]
        return wA_result, wB_result

    def simulate(self):
        start_time = time.time()
        for actor in self.community.actors():
            actor.result_list[:] = []

        # simulate session dialogues
        for channel in self.community.channels():
            self._activate_channel(channel)
        dialog_time = time.time()

        # compute the previous session result for each community actor
        self._compute_results()
        compute_time = time.time()
        print(f"Dialog: {dialog_time - start_time}, Compute: {compute_time - dialog_time}")

    def _compute_results(self):
        for actor in self.community.actors():
            result_list = actor.result_list
            if result_list:
                # actor 'n' participates at least in one dialogue
                ndialogues = len(result_list)
                w = np.zeros(self.community.nvars)
                for wc in result_list:
                    np.add(w, wc, w)
                np.multiply(w, 1.0 / ndialogues, actor.preference)

    def _activate_channel(self, channel):
        if channel.is_active():
            # determine actors participating as Alice and Bob in the
            # current dialogue
            alice, bob = channel.actor1, channel.actor2
            # ------------------------------------------------------
            wA, wB = self._simulate_dialog(channel.dialog_matrix, alice.preference, bob.preference)
            alice.result_list.append(wA)
            bob.result_list.append(wB)
