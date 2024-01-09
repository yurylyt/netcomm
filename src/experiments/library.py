from src.experiments.base import BaseExperiment


class SingleLeaderExperiment(BaseExperiment):
    def configure_community(self):
        # define a leader
        alice = self.netcomm.actor(0)
        alice.confidence = 1.0
        alice.dialog_chance = 1.0
        alice.strong_preference(0)
        alice = self.netcomm.actor(1)
        alice.confidence = 1.0
        alice.dialog_chance = 1.0
        alice.strong_preference(0)

