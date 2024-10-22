from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.schema import Base, ExperimentDTO

engine = create_engine("sqlite:///../../experiments.sqlite", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    exp = ExperimentDTO(
        date=datetime.now(),
        status="init",
        community_size=200,
        iterations_count=10,
        choices=2,
    )
    # iter = Iteration(exp, [1,2,3], 0.5, [4,5,6])
    session.add_all([exp, iter])
    session.commit()
