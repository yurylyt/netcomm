import json
from datetime import datetime
from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.models import Observation


class Base(DeclarativeBase):
    pass


class ExperimentDTO(Base):
    __tablename__ = "experiment"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    date: Mapped[datetime]
    community_size: Mapped[int]
    iterations_count: Mapped[int]
    choices: Mapped[int]
    run_time: Mapped[Optional[int]]
    comment: Mapped[Optional[str]]
    iterations: Mapped[List["Iteration"]] = relationship(back_populates="experiment", cascade="all, delete-orphan")


class Iteration(Base):
    __tablename__ = "iteration"

    def __init__(self, idx, observation):
        super().__init__(
            idx=idx,
            disclaimed=observation.disclaimed,
            preference=json.dumps(observation.preference.tolist()),
            chose=json.dumps(observation.chose.tolist())
        )

    def to_observation(self) -> Observation:
        return Observation(json.loads(self.preference), self.disclaimed, json.loads(self.chose))

    id: Mapped[int] = mapped_column(primary_key=True)
    idx: Mapped[int]
    preference: Mapped[str]
    disclaimed: Mapped[float]
    chose: Mapped[str]
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"))
    experiment: Mapped["ExperimentDTO"] = relationship(back_populates="iterations")

