<<<<<<< HEAD
# DB init and session manager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///data/task_tracker.db")
SessionLocal = sessionmaker(bind=engine)
=======
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

os.makedirs("data", exist_ok=True)
Base = declarative_base()
engine = create_engine("sqlite:///data/task_tracker.db")
SessionLocal = sessionmaker(bind=engine)
>>>>>>> 04823a85d5ccb63ae834837a2cebb3c79d684e24
