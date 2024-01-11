import time

import numpy as np

from src.models import Actor, Observation
from src.models.community import Community
from src.session import Session
from src.utils import preference, bernoulli


class Experiment:
    def __init__(self, iterations, variants=2, community_size=200,
                 rho=20, low_confidence=0.2, high_confidence=0.6, dialog_chance=1.0):
        self.iterations = iterations
        self.netcomm = Community(community_size, nvars=variants)
        self.nvars = variants
        rg = np.random.default_rng()
        for actor in self.netcomm.actors():
            actor.rho = rho
            actor.confidence_level = rg.uniform(low=low_confidence, high=high_confidence)
            actor.dialog_chance = dialog_chance
            actor.is_uncertain(variants)

    def actor(self, idx) -> Actor:
        return self.netcomm.actor(idx)

    def run(self, scribe):
        start_time_total = time.time()
        self.netcomm.init_channels()
        scribe.before(self.poll())
        print("Running experiments, iterations count: ", self.iterations)
        for istep in range(self.iterations):
            if istep % 100 == 0:
                print(f"Done {istep} iterations in {int(time.time() - start_time_total)}s")
            start_time = time.time()
            Session(self.netcomm).simulate()
            session_time = time.time()
            scribe.log_session(istep, self.poll())
            observation_time = time.time()
            # print(f"Session: {session_time - start_time}ms; Observation: {observation_time - session_time}")
        finish_time = time.time()

        running_time = finish_time - start_time_total
        scribe.record_time(int(running_time))
        print(f"Running time: {running_time}s")

        scribe.after()
        return scribe.data_id()

    def poll(self) -> Observation:
        # polling simulation

        # It def belongs here as it's actually a "poll", hence there's some probability of different answers
        # based on preference density.
        disclaimers = 0
        choices = np.zeros(self.nvars)

        for actor in self.netcomm.actors():
            hn = preference.normalized_entropy(actor.preference)
            if bernoulli.trial(np.power(hn, actor.rho)):
                disclaimers += 1  # actor 'n' disclaims a choice
            else:
                # actor 'n' chooses
                choice = np.random.choice(self.nvars, p=actor.preference)
                choices[choice] += 1

        # compute average preference density
        W = np.zeros(self.nvars)
        for actor in self.netcomm.actors():
            np.add(W, actor.preference, W)
        netcomm_size = self.netcomm.size
        np.multiply(W, 1.0 / netcomm_size, W)

        if disclaimers == netcomm_size:  # all actors disclaimed their choice
            return Observation(W, 1.0, preference.uncertainty(self.nvars))

        nondisclaimers = netcomm_size - disclaimers
        np.multiply(choices, 1.0 / nondisclaimers, choices)

        return Observation(W, disclaimers / netcomm_size, choices)
