from nicegui import ui
from db import Base, engine, SessionLocal
from ui.category_tabs import render_category_tabs
from models import Task
from datetime import date

Base.metadata.create_all(bind=engine)

ui.label('Work Task Tracker').classes('text-2xl font-bold p-4')
render_category_tabs()

def check_deadlines():
    session = SessionLocal()
    today = date.today()
    overdue = session.query(Task).filter(Task.deadline < today).count()
    due_today = session.query(Task).filter(Task.deadline == today).count()
    session.close()
    if overdue > 0:
        ui.notify(f'⚠️ {overdue} task(s) overdue!', type='warning', position='top')
    if due_today > 0:
        ui.notify(f'📅 {due_today} task(s) due today.', type='info', position='top')

ui.timer(1.0, check_deadlines, once=True)
ui.timer(120.0, check_deadlines)

ui.run(title='Work Task Tracker')
