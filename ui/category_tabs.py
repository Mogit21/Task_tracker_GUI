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
        with ui.tab_panel(tests_tab): render_task_table('Tests')
        with ui.tab_panel(workorders_tab): render_task_table('Work Orders')
        with ui.tab_panel(tickets_tab): render_task_table('Tickets')

def render_task_table(main_category_filter: str):
    session = SessionLocal()
    categories = session.query(Category).filter_by(main_category=main_category_filter).all()
    session.close()

    with ui.row().classes('w-full p-4 justify-between'):
        ui.button(f'Add {main_category_filter} Task', on_click=lambda: show_add_task_dialog(main_category_filter))

    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'category', 'label': 'Subcategory', 'field': 'category'},
        {'name': 'description', 'label': 'Description', 'field': 'description'},
        {'name': 'priority', 'label': 'Priority', 'field': 'priority'},
        {'name': 'deadline', 'label': 'Deadline', 'field': 'deadline'},
        {'name': 'status', 'label': 'Status', 'field': 'status'},
        {'name': 'actions', 'label': 'Actions'},  # No field: 'actions' to avoid serialization error
    ]
    table = ui.table(columns=columns, rows=[], row_key='id', pagination=10).classes('w-full')

    # @table.add_slot('body-cell-actions')
    # def _(row):
    #     with ui.row().classes('gap-2').on('click.stop', None):
    #         ui.button(icon='edit', on_click=lambda: show_edit_task_dialog(row['id'])).props('flat color=primary')
    #         ui.button(icon='delete', on_click=lambda: confirm_delete(row['id'])).props('flat color=negative')

    with table.add_slot('body-cell-actions'):
        def _(row):
            with ui.row().classes('gap-2').on('click.stop', None):
                ui.button(icon='edit', on_click=lambda: show_edit_task_dialog(row['id'])).props('flat color=primary')
                ui.button(icon='delete', on_click=lambda: confirm_delete(row['id'])).props('flat color=negative')


    def refresh_tasks():
        session = SessionLocal()
        tasks = session.query(Task).join(Category, Task.category_id == Category.id).filter(
            Category.main_category == main_category_filter).all()
        categories = {c.id: c.sub_category for c in session.query(Category).all()}
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

    def confirm_delete(task_id):
        with ui.dialog() as d:
            with ui.card():
                ui.label('Are you sure you want to delete this task?')
                with ui.row():
                    ui.button('Delete', on_click=lambda: do_delete(task_id, d)).props('color=negative')
                    ui.button('Cancel', on_click=d.close)
        d.open()

    def do_delete(task_id, dialog):
        session = SessionLocal()
        session.query(Task).filter(Task.id == task_id).delete()
        session.commit()
        session.close()
        dialog.close()
        refresh_tasks()

    def show_add_task_dialog(main_category):
        dialog = ui.dialog().classes('w-[400px]')
        with dialog, ui.card():
            ui.label(f'Add Task to {main_category}').classes('text-lg')
            session = SessionLocal()
            category_options = {c.sub_category: c.id for c in session.query(Category).filter_by(main_category=main_category).all()}
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
                session.add(Task(
                    category_id=category_options[cat_select.value],
                    description=desc_input.value,
                    priority=prio_select.value,
                    deadline=date.fromisoformat(date_input.value),
                    status=status_select.value
                ))
                session.commit()
                session.close()
                dialog.close()
                refresh_tasks()
        dialog.open()

    def show_edit_task_dialog(task_id):
        session = SessionLocal()
        task = session.query(Task).get(task_id)
        category = session.query(Category).filter_by(id=task.category_id).first()
        category_options = {c.sub_category: c.id for c in session.query(Category).filter_by(main_category=main_category_filter).all()}
        session.close()
        dialog = ui.dialog().classes('w-[400px]')
        with dialog, ui.card():
            ui.label('Edit Task').classes('text-lg')
            ui.label('Subcategory')
            cat_select = ui.select(category_options, value=category.sub_category).classes('w-full')
            ui.label('Description')
            desc_input = ui.input(value=task.description).classes('w-full')
            ui.label('Priority')
            prio_select = ui.select(['High', 'Medium', 'Low'], value=task.priority).classes('w-full')
            ui.label('Deadline')
            date_input = ui.date(value=str(task.deadline)).classes('w-full')
            ui.label('Status')
            status_select = ui.select(['To Do', 'In Progress', 'Done'], value=task.status).classes('w-full')
            with ui.row():
                ui.button('Save', on_click=lambda: save_changes()).props('color=primary')
                ui.button('Cancel', on_click=dialog.close)
            def save_changes():
                session = SessionLocal()
                task = session.query(Task).get(task_id)
                task.description = desc_input.value
                task.priority = prio_select.value
                task.deadline = date.fromisoformat(date_input.value)
                task.status = status_select.value
                task.category_id = category_options[cat_select.value]
                session.commit()
                session.close()
                dialog.close()
                refresh_tasks()
        dialog.open()
