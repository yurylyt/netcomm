import json

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.schema import ExperimentDTO
from src.models import Observation


class DataReader:
    def read(self):
        pass


class PlainReader(DataReader):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        # restore the experiment outcomes
        plain_data = []
        with open(self.filename) as in_file:
            for item in in_file:
                temp = item.split(" ")
                temp = list(map(float, temp))
                plain_data.append(temp)
                del temp
        return plain_data


class JsonReader(DataReader):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename) as in_file:
            json_data = json.load(in_file)
            return [Observation(**data) for data in json_data]


class SqlReader(DataReader):
    def __init__(self, sqlite_uri, experiment_id):
        self.engine = create_engine(sqlite_uri, echo=False)
        self.experiment_id = experiment_id

    def read(self):
        with Session(self.engine) as session:
            return [item.to_observation() for item in session.get(ExperimentDTO, self.experiment_id).iterations]
