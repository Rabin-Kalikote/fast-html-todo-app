from fasthtml.common import *

def render(todo):
    tid = f'todo-{todo.id}'
    
    # Styles
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
    
    tag_style = {
        'dt': 'background-color: #3b82f6; color: white;',  # blue
        'pert': 'background-color: #10b981; color: white;',  # green
        'colt': 'background-color: #8b5cf6; color: white;',  # purple
        'wt': 'background-color: #f97316; color: white;'  # orange
    }
    
    tag_names = {
        'dt': 'Daily Task',
        'pert': 'Personal Task',
        'colt': 'College Task',
        'wt': 'Work Task'
    }
    
    tag_badge = Span(
        tag_names.get(todo.tag, todo.tag),
        style=f'''
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            {tag_style.get(todo.tag, 'background-color: #6b7280; color: white;')}
        '''
    )
    
    button_style = '''
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        border: 1px solid #e5e7eb;
        background-color: white;
        cursor: pointer;
        transition: background-color 0.2s;
    '''
    
    toggle = Button(
        "✓ Complete" if not todo.is_completed else "↺ Undo",
        style=button_style,
        hx_get=f'/toggle/{todo.id}',
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
            Span(f'Created: {todo.c_date}', style='color: #6b7280;'),
            ' | ' if todo.d_date else '',
            Span(f'Due: {todo.d_date}', style='color: #6b7280;') if todo.d_date else '',
            style='font-size: 0.875rem;'
        ),
        style='flex-grow: 1;'
    )
    
    return Li(
        Div(toggle, content, tag_badge, delete, style=todo_style),
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
        create_nav_button('All Tasks', '/lt', active='/lt' in active_route),
        create_nav_button('Completed', '/ct', active='/ct' in active_route),
        create_nav_button('Pending', '/pt', active='/pt' in active_route),
        create_nav_button('By Create Date', '/scd', active='/scd' in active_route),
        create_nav_button('By Due Date', '/sdd', active='/sdd' in active_route),
        style='''
            margin: 1rem 0;
            padding: 0.5rem;
            background-color: #f9fafb;
            border-radius: 0.5rem;
        '''
    )

def create_tags_nav(active_route=''):
    return Div(
        H4('Filter by Tag:', style='margin: 0.5rem 0;'),
        create_nav_button('Daily Tasks', '/dt', active='/dt' in active_route),
        create_nav_button('Personal Tasks', '/pert', active='/pert' in active_route),
        create_nav_button('College Tasks', '/colt', active='/colt' in active_route),
        create_nav_button('Work Tasks', '/wt', active='/wt' in active_route),
        style='''
            margin: 1rem 0;
            padding: 0.5rem;
            background-color: #f9fafb;
            border-radius: 0.5rem;
        '''
    )

app, rt, todos, Todo = fast_app(
    'todos.db',
    render=render,
    id=int,
    title=str,
    body=str,
    c_date=str,
    d_date=str,
    tag=str,
    is_completed=bool,
    pk='id'
)

@rt('/')
def get():
    container_style = '''
        max-width: 800px;
        margin: 2rem auto;
        padding: 1rem;
    '''
    
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
    
    frm = Form(
        Div(
            Input(name='title', placeholder="Enter Task Title", style=input_style),
            Input(name='body', placeholder="Enter Task Description", style=input_style),
            Div(
                Input(name='c_date', type='date', style=input_style),
                Input(name='d_date', type='date', style=input_style),
                style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'
            ),
            Select(
                Option('Daily Task', value='dt'),
                Option('Personal Task', value='pert'),
                Option('College Task', value='colt'),
                Option('Work Task', value='wt'),
                name='tag',
                style=input_style
            ),
            Button('Add Task', style='''
                background-color: #3b82f6;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 0.375rem;
                border: none;
                cursor: pointer;
                width: 100%;
                margin-top: 1rem;
            '''),
            style=form_style,
            hx_post='/',
            target_id="todo-list",
            hx_swap='beforeend'
        )
    )
    
    tdlist = Ul(*todos(), id="todo-list", style='padding: 0;')
    
    return Div(
        H1('Todo List', style='text-align: center; color: #1f2937;'),
        frm,
        create_navigation(),
        create_tags_nav(),
        tdlist,
        style=container_style
    )

@rt('/{tid}')
def delete(tid: int):
    todos.delete(tid)

@rt('/')
def post(title: str, body: str, c_date: str, d_date: str, tag: str):
    new_todo = Todo(
        title=title,
        body=body,
        c_date=c_date,
        d_date=d_date,
        tag=tag,
        is_completed=False
    )
    return todos.insert(new_todo)

@rt('/toggle/{tid}')
def get(tid: int):
    todo = todos[tid]
    todo.is_completed = not todo.is_completed
    todos.update(todo)
    return render(todo)

@rt('/lt')
def get():
    return Div(
        H1('All Tasks', style='text-align: center; color: #1f2937;'),
        create_nav_button('Back to Dashboard', '/'),
        create_navigation('/lt'),
        create_tags_nav(),
        Ul(*todos(), id="todo-list", style='padding: 0;'),
        style='max-width: 800px; margin: 2rem auto; padding: 1rem;'
    )

@rt('/ct')
def get():
    return Div(
        H1('Completed Tasks', style='text-align: center; color: #1f2937;'),
        create_nav_button('Back to Dashboard', '/'),
        create_navigation('/ct'),
        create_tags_nav(),
        Ul(*[todo for todo in todos() if todo.is_completed],
           id="todo-list", style='padding: 0;'),
        style='max-width: 800px; margin: 2rem auto; padding: 1rem;'
    )

@rt('/pt')
def get():
    return Div(
        H1('Pending Tasks', style='text-align: center; color: #1f2937;'),
        create_nav_button('Back to Dashboard', '/'),
        create_navigation('/pt'),
        create_tags_nav(),
        Ul(*[todo for todo in todos() if not todo.is_completed],
           id="todo-list", style='padding: 0;'),
        style='max-width: 800px; margin: 2rem auto; padding: 1rem;'
    )

@rt('/scd')
def get():
    return Div(
        H1('Tasks by Creation Date', style='text-align: center; color: #1f2937;'),
        create_nav_button('Back to Dashboard', '/'),
        create_navigation('/scd'),
        create_tags_nav(),
        Ul(*todos(order_by='c_date'),
           id="todo-list", style='padding: 0;'),
        style='max-width: 800px; margin: 2rem auto; padding: 1rem;'
    )

@rt('/sdd')
def get():
    return Div(
        H1('Tasks by Due Date', style='text-align: center; color: #1f2937;'),
        create_nav_button('Back to Dashboard', '/'),
        create_navigation('/sdd'),
        create_tags_nav(),
        Ul(*[todo for todo in todos(order_by='d_date') if todo.d_date],
           id="todo-list", style='padding: 0;'),
        style='max-width: 800px; margin: 2rem auto; padding: 1rem;'
    )

@rt('/dt')
def get():
    return Div(
        H1('Daily Tasks', style='text-align: center; color: #1f2937;'),
        create_nav_button('Back to Dashboard', '/'),
        create_navigation('/dt'),
        create_tags_nav(),
        Ul(*todos(where="tag='dt'"),
           id="todo-list", style='padding: 0;'),
        style='max-width: 800px; margin: 2rem auto; padding: 1rem;'
    )

@rt('/pert')
def get():
    return Div(
        H1('Personal Tasks', style='text-align: center; color: #1f2937;'),
        create_nav_button('Back to Dashboard', '/'),
        create_navigation('/pert'),
        create_tags_nav(),
        Ul(*todos(where="tag='pert'"),
           id="todo-list", style='padding: 0;'),
        style='max-width: 800px; margin: 2rem auto; padding: 1rem;'
    )

@rt('/colt')
def get():
    return Div(
        H1('College Tasks', style='text-align: center; color: #1f2937;'),
        create_nav_button('Back to Dashboard', '/'),
        create_navigation('/colt'),
        create_tags_nav(),
        Ul(*todos(where="tag='colt'"),
           id="todo-list", style='padding: 0;'),
        style='max-width: 800px; margin: 2rem auto; padding: 1rem;'
    )

@rt('/wt')
def get():
    return Div(
        H1('Work Tasks', style='text-align: center; color: #1f2937;'),
        create_nav_button('Back to Dashboard', '/'),
        create_navigation('/wt'),
        create_tags_nav(),
        Ul(*todos(where="tag='wt'"),
           id="todo-list", style='padding: 0;'),
        style='max-width: 800px; margin: 2rem auto; padding: 1rem;'
    )

serve()