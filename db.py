# DB init and session manager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///data/task_tracker.db")
SessionLocal = sessionmaker(bind=engine)
