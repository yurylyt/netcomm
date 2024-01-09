from datetime import datetime

from src.models.community import Community
import json


class Observer:
    def __init__(self):
        self._netcomm = None

    def set_netcomm(self, netcomm):
        self._netcomm = netcomm

    def before(self):
        pass

    def observe_session(self, index):
        pass

    def after(self):
        pass


class SimpleObserver(Observer):
    def __init__(self):
        super().__init__()
        self._protocol = []

    def _filename(self):
        return "protocol.dat"

    def before(self):
        self._protocol.append(self._netcomm.observe())

    def observe_session(self, index):
        observation = self._netcomm.observe()
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


class JsonObserver(SimpleObserver):
    def __init__(self, niter):
        super().__init__()
        self._niter = niter

    def _filename(self):
        datestr = datetime.now().strftime("%Y-%m-%d_%H:%M")
        return f"data/{datestr}_s{self._netcomm.size}_i{self._niter}_c{self._netcomm.nvars}.json"

    def after(self):
        print("Storing results as json")
        with open(self._filename(), "w") as out_file:
            json_str = json.dumps([to_dict(p) for p in self._protocol])
            json_str = "},\n".join(json_str.split("},"))  # each object on a new line for readability
            out_file.writelines(json_str)


