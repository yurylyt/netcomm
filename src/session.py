from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

import numpy as np

from src.models.community import Community


def simulate(community: Community):
    community.clear_results()

    # simulate session dialogues
    for channel in community.channels():
        _activate_channel(channel)

    # compute the previous session result for each community actor
    _compute_results(community)


def _activate_channel(channel):
    if channel.is_active():
        # determine actors participating as Alice and Bob in the current dialogue
        alice, bob = channel.actor1, channel.actor2
        # ------------------------------------------------------
        wA, wB = _simulate_dialog(channel.dialog_matrix, alice.preference, bob.preference)
        alice.result_list.append(wA)
        bob.result_list.append(wB)


def _simulate_dialog(D, wA, wB):
    # get dialogue matrix of the current dialogue and
    # the preference densities of its participants
    nvars = 2
    wA_result = np.zeros(nvars)
    wB_result = np.zeros(nvars)
    for v in range(nvars):
        wA_result[v] = D[0, 0] * wA[v] + D[0, 1] * wB[v]
        wB_result[v] = D[1, 0] * wA[v] + D[1, 1] * wB[v]
    return wA_result, wB_result


def _compute_results(community):
    for actor in community.actors():
        result_list = actor.result_list
        if result_list:
            # actor 'n' participates at least in one dialogue
            ndialogues = len(result_list)
            w = np.zeros(community.nvars)
            for wc in result_list:
                np.add(w, wc, w)
            np.multiply(w, 1.0 / ndialogues, actor.preference)



