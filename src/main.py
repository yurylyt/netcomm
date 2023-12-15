from src.experiments import SingleLeaderExperiment
from src.observer import JsonObserver

if __name__ == '__main__':
    niter = 1000
    experiment = SingleLeaderExperiment(
        iterations=niter,
        variants=2,
        observer=JsonObserver(niter)
    )
    experiment.run()
