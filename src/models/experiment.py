import numpy as np

from src.models.community import Community
from src.models.actor import Actor


class Experiment:
    def __init__(self, name, iterations,
                 variants=2,
                 community_size=200,
                 low_decisiveness=3,
                 high_decisiveness=3,
                 low_confidence=0.2,
                 high_confidence=0.6,
                 dialog_chance=1.0):
        self.name = name
        self.iterations = iterations
        self.netcomm = Community(community_size, nvars=variants)
        self.nvars = variants
        rg = np.random.default_rng()
        for actor in self.netcomm.actors():
            actor.decisiveness = rg.uniform(low=low_decisiveness, high=high_decisiveness)
            actor.confidence_level = rg.uniform(low=low_confidence, high=high_confidence)
            actor.dialog_chance = dialog_chance
            actor.is_uncertain(variants)

    def actor(self, idx) -> Actor:
        return self.netcomm.actor(idx)
