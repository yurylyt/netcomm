from src.experiments import SingleLeaderExperiment

if __name__ == '__main__':
    experiment = SingleLeaderExperiment(
        iterations=100,
        variants=2
    )
    experiment.run()






