# Task_tracker_GUI



# Component architecture

+---------------------+
|  Web UI (NiceGUI)   |
+---------------------+
        |
        v
+----------------------+
| Task Controller      |  ← Handles routing, validation, filters
+----------------------+
        |
        v
+---------------------+
| SQLite DB (via SQLAlchemy) |
+---------------------+


# UI Structure
Left Panel: Filters

Category & Subcategory

Status

Priority

Main Panel: Task Table View

With sorting, search

Buttons: Add / Edit / Delete

Dialog: Form to create or edit tasks

# Example Task Flow:

@startuml
start
:User opens web app;
:Clicks 'Add Task';
:Select category & subcategory;
:Fill description, priority, deadline, status;
:Submit form;
:Controller validates and inserts into DB;
:Task list refreshes;
stop
@enduml

1. Environment Setup
   
   python3 -m venv venv
    source venv/bin/activate
    pip install nicegui sqlalchemy






python main.py

Then visit: http://localhost:8080





python seed_categories.py
This script inserts predefined categories into your SQLite database so that your task UI has valid options to choose from when creating tasks.

When should I run this?
Only once — after your database is initialized but before using the UI. If you run it again, it won’t create duplicates because of the if not exists check.

📦 controllers.py: When to Use It
Right now, all the logic (e.g., saving tasks, refreshing lists) is inside your UI code (task_table.py). This works, but as your app grows, that logic might get messy.

You can move business logic to controllers.py to:

✅ Keep UI code clean
✅ Make logic reusable (e.g., for future API or CLI use)
✅ Make unit testing easier

