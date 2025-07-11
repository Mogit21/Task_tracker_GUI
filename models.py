<<<<<<< HEAD
# SQLAlchemy models

from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from db import Base

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    main_category = Column(String, nullable=False)
    sub_category = Column(String, nullable=False)

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    description = Column(String, nullable=False)
    priority = Column(String, CheckConstraint("priority IN ('High', 'Medium', 'Low')"), nullable=False)
    deadline = Column(Date, nullable=False)
    status = Column(String, CheckConstraint("status IN ('To Do', 'In Progress', 'Done')"), nullable=False)
=======
from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from db import Base

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    main_category = Column(String, nullable=False)
    sub_category = Column(String, nullable=False)

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    description = Column(String, nullable=False)
    priority = Column(String, CheckConstraint("priority IN ('High', 'Medium', 'Low')"), nullable=False)
    deadline = Column(Date, nullable=False)
    status = Column(String, CheckConstraint("status IN ('To Do', 'In Progress', 'Done')"), nullable=False)
>>>>>>> 04823a85d5ccb63ae834837a2cebb3c79d684e24
