from fasthtml import FastHTML
from database.models import db, TodoItem
from routes.todos import todos_bp

app = FastHTML(__name__)

# Initialize the database
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(todos_bp)

if __name__ == "__main__":
    app.run(debug=True)