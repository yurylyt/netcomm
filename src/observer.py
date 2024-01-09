from datetime import datetime

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.schema import Base, Experiment, Iteration


class Observer:
    def __init__(self, experiment):
        self._experiment = experiment

    def before(self, observation):
        pass

    def observe_session(self, index, observation):
        pass

    def after(self):
        pass

# deprecated
class SimpleObserver(Observer):
    def __init__(self, experiment):
        super().__init__(experiment)
        self._protocol = []

    def _filename(self):
        return "protocol.dat"

    def before(self, observation):
        self._protocol.append(observation)

    def observe_session(self, index, observation):
        # print(f"#{index}: {observation}")
        self._protocol.append(observation)

    def after(self):
        print(f"Storing the experiment results ({len(self._protocol)})...")
        with open(self._filename(), "w") as out_file:
            out_file.writelines([str(item) + '\n' for item in self._protocol])


def to_dict(observation):
    return {
        "preference": observation.preference.tolist(),
        "disclaimed": observation.disclaimed,
        "chose": observation.chose.tolist()
    }


# deprecated
class JsonObserver(SimpleObserver):
    def _filename(self):
        datestr = datetime.now().strftime("%Y-%m-%d_%H:%M")
        return f"data/{datestr}_s{self._experiment.netcomm.size}_i{self._experiment.iterations}_c{self._experiment.netcomm.nvars}.json"

    def after(self):
        print("Storing results as json")
        with open(self._filename(), "w") as out_file:
            json_str = json.dumps([to_dict(p) for p in self._protocol])
            json_str = "},\n".join(json_str.split("},"))  # each object on a new line for readability
            out_file.writelines(json_str)


class SQLObserver(Observer):

    def __init__(self, experiment):
        super().__init__(experiment)
        engine = create_engine("sqlite:///experiments.sqlite", echo=False)
        Base.metadata.create_all(engine)
        exp_dto = Experiment(
            date=datetime.now(),
            status="init",
            community_size=experiment.netcomm.size,
            iterations_count=experiment.iterations,
            choices=experiment.netcomm.nvars
        )
        self._session = Session(engine)
        self._session.add(exp_dto)
        self._session.commit()
        self._exp_dto = exp_dto

    def before(self, observation):
        self._exp_dto.status = 'running'
        self.observe_session(0, observation)

    def observe_session(self, index, observation):
        self._exp_dto.iterations.append(Iteration(index + 1, observation))
        self._session.commit()

    def after(self):
        self._exp_dto.status = 'done'
        self._session.commit()
        self._session.close()
