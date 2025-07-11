import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

os.makedirs("data", exist_ok=True)
Base = declarative_base()
engine = create_engine("sqlite:///data/task_tracker.db")
SessionLocal = sessionmaker(bind=engine)
