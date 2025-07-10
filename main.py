# Entry point for NiceGUI app

from nicegui import ui
from db import Base, engine
from models import Category, Task

from ui.category_tabs import render_category_tabs
render_category_tabs()


# Initialize database
Base.metadata.create_all(bind=engine)

ui.label('Work Task Tracker').classes('text-2xl font-bold p-4')
# Add call to UI component (later in ui/task_table.py)
# from ui.task_table import render_task_table
# render_task_table()

ui.run(title='Work Task Tracker')
