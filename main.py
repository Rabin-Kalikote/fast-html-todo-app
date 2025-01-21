from fasthtml.common import *
from datetime import datetime

# App initialization
app,rt,todos,Todo = fast_app(
    'data/todos.db',
    hdrs=[
        Style(':root { --pico-font-size: 100%; }'),
        Link(rel="stylesheet", href="/static/styles.css")
    ],
    id=int,
    title=str,
    body=str,
    created_at=datetime,
    due_date=datetime,
    is_completed=bool,
    tags=str,
    pk='id'
)

# Constants
id_curr = 'current-todo'
def tid(id): return f'todo-{id}'

# Todo item display
@patch
def __ft__(self:Todo):
    show = AX(self.title, f'/todos/{self.id}', id_curr)
    edit = AX('edit', f'/edit/{self.id}', id_curr)
    status = ' ✅' if self.is_completed else ''
    tags = [Span(tag.strip(), cls='tag', hx_get=f'/filter/tag/{tag.strip()}') 
            for tag in (self.tags or '').split(',') if tag.strip()]
    
    return Li(
        Div(show, status, cls='todo-header'),
        Div(self.body, cls='todo-body'),
        Div(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}"),
        Div(f"Due: {self.due_date.strftime('%Y-%m-%d') if self.due_date else 'No due date'}"),
        Div(*tags, cls='tags'),
        Div(edit, cls='todo-actions'),
        id=tid(self.id)
    )

# Form components
def mk_form(**kw):
    return Group(
        Input(id="title", name="title", placeholder="Title", required=True),
        Textarea(id="body", name="body", placeholder="Description"),
        Input(id="due_date", name="due_date", type="date"),
        Input(id="tags", name="tags", placeholder="Tags (comma-separated)"),
        **kw
    )

@rt("/")
def get():
    filters = Div(
        Button("All", hx_get="/", cls="active"),
        Button("Active", hx_get="/filter/status/active"),
        Button("Completed", hx_get="/filter/status/completed"),
        cls="filters"
    )
    
    sorts = Div(
        Button("By Created", hx_get="/filter/sort/created", cls="active"),
        Button("By Due Date", hx_get="/filter/sort/due"),
        cls="sorts"
    )
    
    add_form = Form(
        mk_form(),
        Button("Add Todo"),
        hx_post="/",
        hx_target="#todo-list",
        hx_swap="beforeend"
    )
    
    return Title("Todo Tracker"), Main(
        H1("Todo Tracker"),
        Card(
            filters,
            sorts,
            add_form,
            Ul(*todos(), id='todo-list'),
            footer=Div(id=id_curr)
        ),
        cls='container'
    )

@rt("/todos/{id}")
def delete(id:int):
    todos.delete(id)
    return clear(id_curr)

@rt("/")
def post(todo:Todo):
    todo.created_at = datetime.now()
    return todos.insert(todo), mk_form(hx_swap_oob='true')

@rt("/edit/{id}")
def get(id:int):
    todo = todos.get(id)
    res = Form(
        mk_form(),
        Hidden(id="id"),
        CheckboxX(id="is_completed", label='Completed'),
        Button("Save"),
        hx_put="/",
        hx_swap="outerHTML",
        target_id=tid(id),
        id="edit"
    )
    return fill_form(res, todo)

@rt("/todos/{id}")
def get(id:int):
    todo = todos.get(id)
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=tid(todo.id), hx_swap="outerHTML")
    return Div(
        Div(todo.title),
        Div(todo.body),
        btn
    )

@rt("/filter/status")
def get(status: str):
    items = list(todos())
    if status == "Completed":
        items = [t for t in items if t.is_completed]
    elif status == "Active":
        items = [t for t in items if not t.is_completed]
    return Ul(*items, id='todo-list')

@rt("/filter/sort")
def get(sort: str):
    items = list(todos())
    if sort == "Due Date":
        items.sort(key=lambda x: x.due_date or datetime.max)
    else:
        items.sort(key=lambda x: x.created_at)
    return Ul(*items, id='todo-list')

@rt("/filter/tag/{tag}")
def get(tag: str):
    items = [t for t in todos() if tag in (t.tags or '').split(',')]
    return Ul(*items, id='todo-list')

@rt("/toggle/{id}")
def put(id: int):
    todo = todos.get(id)
    todo.is_completed = not todo.is_completed
    todos.upsert(todo)
    return todo

serve()