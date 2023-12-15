import time

from src.models.community import Community
from src.observer import SimpleObserver
from src.session import Session


class BaseExperiment:
    def __init__(self, iterations, variants, observer=SimpleObserver()):
        self._iterations = iterations
        self._netcomm = Community(200, nvars=variants)
        self._configure_community()
        self._netcomm.build_channels()
        self._observer = observer
        self._observer.set_netcomm(self._netcomm)

    def _configure_community(self):
        pass

    def run(self):
        start_time_total = time.time()
        self._observer.before()
        print("Running experiments, iterations count: ", self._iterations)
        for istep in range(self._iterations):
            if istep % 100 == 0:
                print("Done iterations: ", istep)
            start_time = time.time()
            Session(self._netcomm).simulate()
            session_time = time.time()
            self._observer.observe_session(istep)
            observation_time = time.time()
            print(f"Session: {session_time - start_time}ms; Observation: {observation_time - session_time}")
        running_time = time.time()

        self._observer.after()

        print(f"Running time: {running_time - start_time_total}ms")

