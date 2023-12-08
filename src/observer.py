from src.models.community import Community


class Observer:
    def __init__(self, netcomm: Community):
        self._netcomm = netcomm

    def before(self):
        pass

    def observe_session(self, index):
        pass

    def after(self):
        pass


class SimpleObserver(Observer):
    def __init__(self, netcomm, filename="protocol.dat"):
        super().__init__(netcomm)
        self._protocol = []
        self._filename = filename

    def before(self):
        self._protocol.append(self._netcomm.observe())

    def observe_session(self, index):
        observation = self._netcomm.observe()
        print(f"#{index}: {observation}")
        self._protocol.append(observation)

    def after(self):
        print(f"Storing the experiment results ({len(self._protocol)})...")
        out_file = open(self._filename, "w")
        out_file.writelines([str(item) + '\n' for item in self._protocol])
        out_file.close()

