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
    # Handle created_at display safely
    created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M') if isinstance(self.created_at, datetime) else "No date"
    return Div(
        show,
        edit,
        Div(f"Created: {created_at_str}"),
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
async def delete(id:int):
    # Use synchronous delete
    todos.delete(id)
    return clear(id_curr)

@rt("/")
async def post(req: Request):
    form = await req.form()
    
    # Create new todo with proper datetime handling
    todo = Todo(
        title=form.get('title'),
        body=form.get('body'),
        created_at=datetime.now(),
        due_date=datetime.strptime(form.get('due_date'), '%Y-%m-%d') if form.get('due_date') else None,
        tags=form.get('tags'),
        is_completed=False
    )
    
    # Use synchronous insert
    todos.insert(todo)
    return todo.__ft__()

@rt("/edit/{id}")
async def get(id:int):
    # Use synchronous get
    todo = todos.get(id)
    res = Form(
        mk_form(),
        Hidden(name="id", value=todo.id),
        CheckboxX(id="is_completed", checked=todo.is_completed, label='Completed'),
        Button("Save"),
        hx_put=f"/edit/{id}",
        hx_swap="outerHTML",
        target_id=tid(id)
    )
    return res.fill(todo)

# @rt("/todos/{id}")
# def get(id:int):
#     todo = todos.get(id)
#     btn = Button('delete', hx_delete=f'/todos/{todo.id}',
#                  target_id=tid(todo.id), hx_swap="outerHTML")
#     return Div(
#         Div(todo.title),
#         Div(todo.body),
#         btn
#     )

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