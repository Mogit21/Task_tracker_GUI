from nicegui import ui
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Task, Category
from datetime import date

def render_category_tabs():
    with ui.tabs().classes('w-full') as tabs:
        tests_tab = ui.tab('Tests')
        workorders_tab = ui.tab('Work Orders')
        tickets_tab = ui.tab('Tickets')

    with ui.tab_panels(tabs, value=tests_tab).classes('w-full'):
        with ui.tab_panel(tests_tab):
            render_task_table('Tests')
        with ui.tab_panel(workorders_tab):
            render_task_table('Work Orders')
        with ui.tab_panel(tickets_tab):
            render_task_table('Tickets')

def render_task_table(main_category_filter: str):
    session = SessionLocal()
    categories = session.query(Category).filter_by(main_category=main_category_filter).all()
    cat_map = {c.id: f"{c.main_category} > {c.sub_category}" for c in categories}
    session.close()

    with ui.row().classes('w-full p-4 justify-between'):
        ui.button(f'Add {main_category_filter} Task', on_click=lambda: show_add_task_dialog(main_category_filter))

    table = ui.table(columns=[
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'category', 'label': 'Category', 'field': 'category'},
        {'name': 'description', 'label': 'Description', 'field': 'description'},
        {'name': 'priority', 'label': 'Priority', 'field': 'priority'},
        {'name': 'deadline', 'label': 'Deadline', 'field': 'deadline'},
        {'name': 'status', 'label': 'Status', 'field': 'status'},
    ], rows=[], row_key='id', pagination=10).classes('w-full')

    def refresh_tasks():
        session = SessionLocal()
        tasks = (
            session.query(Task)
            .join(Category, Task.category_id == Category.id)
            .filter(Category.main_category == main_category_filter)
            .all()
        )
        categories = {c.id: f"{c.main_category} > {c.sub_category}" for c in session.query(Category).all()}
        session.close()
        table.rows = [{
            'id': t.id,
            'category': categories.get(t.category_id, 'Unknown'),
            'description': t.description,
            'priority': t.priority,
            'deadline': t.deadline.strftime('%Y-%m-%d'),
            'status': t.status
        } for t in tasks]

    refresh_tasks()

    def show_add_task_dialog(main_category):
        dialog = ui.dialog().classes('w-[400px]')
        with dialog, ui.card():
            ui.label(f'Add Task to {main_category}').classes('text-lg')

            # session = SessionLocal()
            # category_options = {
            #     f"{c.main_category} > {c.sub_category}": c.id
            #     for c in session.query(Category).filter_by(main_category=main_category).all()
            # }
            # session.close()

            # ui.label('Category')
            # cat_select = ui.select(category_options).classes('w-full')
            session = SessionLocal()
            category_options = {
                c.sub_category: c.id
                for c in session.query(Category).filter_by(main_category=main_category).all()
            }
            session.close()

            ui.label('Subcategory')
            cat_select = ui.select(category_options).classes('w-full')


            ui.label('Description')
            desc_input = ui.input().classes('w-full')

            ui.label('Priority')
            prio_select = ui.select(['High', 'Medium', 'Low']).classes('w-full')

            ui.label('Deadline')
            date_input = ui.date(value=str(date.today())).classes('w-full')

            ui.label('Status')
            status_select = ui.select(['To Do', 'In Progress', 'Done']).classes('w-full')

            with ui.row():
                ui.button('Save', on_click=lambda: save_task()).props('color=primary')
                ui.button('Cancel', on_click=dialog.close)

            def save_task():
                session = SessionLocal()
                task = Task(
                    category_id=category_options[cat_select.value],
                    description=desc_input.value,
                    priority=prio_select.value,
                    deadline=date.fromisoformat(date_input.value),
                    status=status_select.value
                )
                session.add(task)
                session.commit()
                session.close()
                dialog.close()
                refresh_tasks()

        dialog.open()
