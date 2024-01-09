from src.experiments import SingleLeaderExperiment
from src.observer import SQLObserver

if __name__ == '__main__':
    niter = 1000
    experiment = SingleLeaderExperiment(
        iterations=niter,
        variants=2,
        observer=SQLObserver
    )
    experiment.run()
