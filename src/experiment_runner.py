import time

import numpy as np

from models import Observation
from models.community import Community
from utils import preference, bernoulli


def run_experiment(experiment, observer):
    start_time_total = time.time()
    experiment.netcomm.init_channels()
    observer.before(_poll_community(experiment))
    print("Running experiments, iterations count: ", experiment.iterations)
    for istep in range(experiment.iterations):
        if istep % 100 == 0:
            print(f"Done {istep} iterations in {int(time.time() - start_time_total)}s")
        start_time = time.time()
        _simulate_session(experiment.netcomm)
        session_time = time.time()
        observer.log_session(istep, _poll_community(experiment))
        observation_time = time.time()
        # print(f"Session: {session_time - start_time}ms; Observation: {observation_time - session_time}")
    finish_time = time.time()

    running_time = finish_time - start_time_total
    observer.record_time(int(running_time))
    print(f"Running time: {running_time}s")

    observer.after()
    return observer.data_id()


def _poll_community(experiment) -> Observation:
    # polling simulation

    # It def belongs here as it's actually a "poll", hence there's some probability of different answers
    # based on preference density.
    netcomm = experiment.netcomm
    disclaimers = 0
    choices = np.zeros(experiment.nvars)

    for actor in netcomm.actors():
        decision = actor.make_decision()
        if decision == preference.DISCLAIMER:
            disclaimers += 1
        else:
            choices[decision] += 1

    # compute average preference density
    W = np.zeros(experiment.nvars)
    for actor in netcomm.actors():
        np.add(W, actor.preference, W)
    netcomm_size = netcomm.size
    np.multiply(W, 1.0 / netcomm_size, W)

    if disclaimers == netcomm_size:  # all actors disclaimed their choice
        return Observation(W, 1.0, preference.uncertainty(experiment.nvars))

    nondisclaimers = netcomm_size - disclaimers
    np.multiply(choices, 1.0 / nondisclaimers, choices)

    return Observation(W, disclaimers / netcomm_size, choices)


def _simulate_session(community: Community):
    results = [[] for _ in range(community.size)]

    for channel in community.active_channels():
        wA, wB = channel.activate()
        # ------------------------------------------------------
        results[channel.actor1.node].append(wA)
        results[channel.actor2.node].append(wB)

    # compute the previous session result for each community actor
    _compute_results(community, results)


def _compute_results(community, results):
    for i, actor in enumerate(community.actors()):
        result_list = results[i]
        if result_list:
            # actor 'n' participates at least in one dialogue
            ndialogues = len(result_list)
            w = np.zeros(community.nvars)
            for wc in result_list:
                np.add(w, wc, w)
            np.multiply(w, 1.0 / ndialogues, actor.preference)
