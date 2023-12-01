import threading
import time
import numpy as np


class Session:
    """
    Session simulator
    """

    def __init__(self, community):
        self.community = community
        self._results = [[] for _ in range(self.community.size)]

    def _simulate_dialog(self, D, wA, wB):
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

        # simulate session dialogues
        for channel in self.community.channels():
            self._activate_channel(channel)
        dialog_time = time.time()

        # compute the previous session result for each community actor
        self._compute_results()
        compute_time = time.time()
        print(f"Dialog: {dialog_time - start_time}, Compute: {compute_time - dialog_time}")

    def _compute_results(self):
        for i, result in enumerate(self._results):
            if result:
                # actor 'n' participates at least in one dialogue
                ndialogues = len(result)
                w = np.zeros(self.community.nvars)
                for wc in result:
                    np.add(w, wc, w)
                np.multiply(w, 1.0 / ndialogues, self.community.actor(i).w)

    def _activate_channel(self, channel):
        if channel.is_active():
            # determine actors participating as Alice and Bob in the
            # current dialogue
            alice_idx, bob_idx = channel.actor1, channel.actor2
            alice = self.community.actor(alice_idx)
            bob = self.community.actor(bob_idx)
            # ------------------------------------------------------
            wA, wB = self._simulate_dialog(channel.D, alice.w, bob.w)
            self._results[channel.actor1].append(wA)
            self._results[channel.actor2].append(wB)
