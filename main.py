from fasthtml.common import *
from datetime import datetime

def render(todo):
    tid = f'todo-{todo.id}'

    created_at = todo.created_at
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    
    due_date = todo.due_date
    if isinstance(due_date, str) and due_date:
        due_date = datetime.fromisoformat(due_date)
        
    content = Div(
        H3(todo.title, style='margin: 0; font-size: 1.125rem;'),
        P(todo.body, style='margin: 0.5rem 0; color: #4b5563;'),
        Div(
            Span(f'Created: {created_at.strftime("%Y-%m-%d %H:%M")}', style='color: #6b7280;'),
            ' | ' if due_date else '',
            Span(f'Due: {due_date.strftime("%Y-%m-%d")}', style='color: #6b7280;') if due_date else '',
            style='font-size: 0.875rem;'
        ),
        style='flex-grow: 1;'
    )
    
    todo_style = '''
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        background-color: white;
        display: flex;
        align-items: center;
        gap: 1rem;
    '''
    
    button_style = '''
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        border: 1px solid #e5e7eb;
        background-color: white;
        cursor: pointer;
        transition: background-color 0.2s;
    '''
    
    tags = todo.tags.split(',') if todo.tags else []
    tag_badges = [
        Span(
            tag.strip(),
            style='''
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.875rem;
                background-color: #6b7280;
                color: white;
                margin-right: 0.5rem;
            '''
        ) for tag in tags
    ]
    
    toggle = Button(
        "✓ Complete" if not todo.is_completed else "↺ Undo",
        style=button_style,
        hx_post=f'/toggle/{todo.id}',
        target_id=tid
    )
    
    delete = Button(
        "🗑 Delete",
        style=f'{button_style} color: #ef4444;',
        hx_delete=f'/{todo.id}',
        hx_swap='outerHTML',
        target_id=tid
    )
    
    title_style = 'text-decoration: line-through;' if todo.is_completed else ''
    content = Div(
        H3(todo.title, style=f'margin: 0; font-size: 1.125rem; {title_style}'),
        P(todo.body, style='margin: 0.5rem 0; color: #4b5563;'),
        Div(
            Span(f'Created: {datetime.fromisoformat(todo.created_at).strftime("%Y-%m-%d %H:%M")}', style='color: #6b7280;'),
            ' | ' if todo.due_date else '',
            Span(f'Due: {datetime.fromisoformat(todo.due_date).strftime("%Y-%m-%d %H:%M")}', style='color: #6b7280;') if todo.due_date else '',
            style='font-size: 0.875rem;'
        ),
        Div(*tag_badges, style='margin-top: 0.5rem;'),
        style='flex-grow: 1;'
    )
    
    return Li(
        Div(toggle, content, delete, style=todo_style),
        id=tid,
        style='list-style: none;'
    )

def create_nav_button(text, href, active=False):
    style = f'''
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        border: 1px solid #e5e7eb;
        background-color: {'#f3f4f6' if active else 'white'};
        text-decoration: none;
        color: inherit;
        display: inline-block;
        margin: 0.25rem;
    '''
    return Button(A(text, href=href, style='text-decoration: none; color: inherit;'), style=style)

def create_navigation(active_route=''):
    return Div(
        create_nav_button('All Tasks', '/', active='/' == active_route),
        create_nav_button('Completed', '/completed', active='/completed' == active_route),
        create_nav_button('Pending', '/pending', active='/pending' == active_route),
        create_nav_button('By Due Date', '/by-due-date', active='/by-due-date' == active_route),
        style='''
            margin: 1rem 0;
            padding: 0.5rem;
            background-color: #f9fafb;
            border-radius: 0.5rem;
        '''
    )

# Initialize app
app, rt, todos, Todo = fast_app(
    'todos.db',
    render=render,
    id=int,
    title=str,
    body=str,
    tags=str,
    created_at=datetime,
    due_date=datetime,
    is_completed=bool,
    pk='id'
)

@rt('/')
def get():
    container_style = 'max-width: 800px; margin: 2rem auto; padding: 1rem;'
    
    form_style = '''
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    '''
    
    input_style = '''
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.375rem;
        margin: 0.5rem 0;
    '''
    
    button_style = '''
        background-color: #3b82f6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        border: none;
        cursor: pointer;
        width: 100%;
        margin-top: 1rem;
    '''
    
    frm = Form(
        Input(name='title', placeholder="Task Title", required=True, style=input_style),
        Input(name='body', placeholder="Task Description", style=input_style),
        Input(name='tags', placeholder="Tags (comma-separated)", style=input_style),
        Input(name='due_date', type='date', style=input_style),
        Button('Add Task', style=button_style),
        style=form_style,
        hx_post='/',
        target_id="todo-list",
        hx_swap='beforeend'
    )
    
    tdlist = Ul(*todos(), id="todo-list", style='padding: 0;')
    
    return Div(
        H1('Todo App', style='text-align: center; color: #1f2937;'),
        frm,
        create_navigation(),
        tdlist,
        style=container_style
    )

@rt('/')
def post(title: str, body: str, tags: str = '', due_date: str = None):
    # Ensure proper datetime handling
    todo = Todo(
        title=title,
        body=body,
        tags=tags,
        created_at=datetime.now().isoformat(),
        due_date=datetime.strptime(due_date, '%Y-%m-%d').isoformat() if due_date else None,
        is_completed=False
    )
    todos.insert(todo)
    return todo.__ft__()

@rt('/toggle/{id}')
def post(id: int):
    todo = todos[id]
    todo.is_completed = not todo.is_completed
    todos.update(todo)
    return todo.__ft__()

@rt('/{id}')
def delete(id: int):
    todos.delete(id)
    return ''

@rt('/completed')
def get():
    completed = [t for t in todos() if t.is_completed]
    return Div(
        H1('Completed Tasks', style='text-align: center; color: #1f2937;'),
        create_navigation('/completed'),
        Ul(*completed, style='padding: 0;')
    )

@rt('/pending')
def get():
    pending = [t for t in todos() if not t.is_completed]
    return Div(
        H1('Pending Tasks', style='text-align: center; color: #1f2937;'),
        create_navigation('/pending'),
        Ul(*pending, style='padding: 0;')
    )

@rt('/by-due-date')
def get():
    sorted_todos = sorted(
        [t for t in todos() if t.due_date], 
        key=lambda x: x.due_date
    )
    return Div(
        H1('Tasks by Due Date', style='text-align: center; color: #1f2937;'),
        create_navigation('/by-due-date'),
        Ul(*sorted_todos, style='padding: 0;')
    )

if __name__ == '__main__':
    serve()