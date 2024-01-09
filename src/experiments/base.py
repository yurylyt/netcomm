import time

from src.models.community import Community
from src.observer import SimpleObserver
from src.session import Session


class BaseExperiment:
    def __init__(self, iterations, variants, community_size=200, observer=SimpleObserver):
        self.iterations = iterations
        self.netcomm = Community(community_size, nvars=variants)
        self.configure_community()
        self.netcomm.build_channels()
        self._observer = observer(self)

    def configure_community(self):
        pass

    def run(self):
        start_time_total = time.time()
        self._observer.before(self.netcomm.poll())
        print("Running experiments, iterations count: ", self.iterations)
        for istep in range(self.iterations):
            if istep % 100 == 0:
                print(f"Done {istep} iterations in {int(time.time() - start_time_total)}s")
            start_time = time.time()
            Session(self.netcomm).simulate()
            session_time = time.time()
            self._observer.observe_session(istep, self.netcomm.poll())
            observation_time = time.time()
            # print(f"Session: {session_time - start_time}ms; Observation: {observation_time - session_time}")
        running_time = time.time()

        self._observer.after()

        print(f"Running time: {running_time - start_time_total}s")

