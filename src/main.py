from src.experiments import SingleLeaderExperiment
from src.observer import JsonObserver

if __name__ == '__main__':
    experiment = SingleLeaderExperiment(
        iterations=100,
        variants=2,
        observer=JsonObserver
    )
    experiment.run()
