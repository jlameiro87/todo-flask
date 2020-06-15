import os

from flask import Flask, session, render_template, request, jsonify, redirect
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from flask_sqlalchemy import SQLAlchemy
from models import User, ToDo, Base

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# To persist in db the model changes
# engine = create_engine(os.getenv("DATABASE_URL"))
# Base.metadata.create_all(engine)

INDEX = "index.html"
REGISTER = "register.html"
LOGIN = "login.html"
PROFILE = "profile.html"
TODOS = "todos.html"

# Default route
@app.route("/")
def index():
    if "user" not in session.keys() or session["user"] is None:
        return render_template(LOGIN)
    else:
        # get todos and count it by pending & completed
        pending = 0
        completed = 0
        records = db.session.query(ToDo).filter(ToDo.user_id==session["user"].id).all()
        for record in records:
            if record.status == True:
                completed = completed + 1
            else:
                pending = pending + 1
        
        return render_template(INDEX, pending=pending, completed=completed)

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # register user in db
        
        # get form information.
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")
        email = request.form.get("email")

        # Ensure all required data was submitted
        if not first_name or not last_name or not username or not password or not password_confirmation or not email:
            return render_template(REGISTER, error=True, message="You must provide all the required data")
        else:
            user = User(first_name=first_name, last_name=last_name, username=username, password=generate_password_hash(password), email=email)
            db.session.add(user)
            db.session.commit()
            return render_template(REGISTER, success=True, message="User registered susccessfully")
    else:
        return render_template(REGISTER)

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # login user in the system
        
        # get form information.
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure all required data was submitted
        if not username or not password:
            return render_template(LOGIN, error=True, message="You must provide all the required data")
        else:
            user = db.session.query(User).filter(User.username==username).first()
            if user is None or not check_password_hash(user.password, password):
                return render_template(LOGIN, error=True, message="Invalid username or password")
            else:
                session["user"] = user
            
                # Redirect user to index page
                return redirect("/")
    else:
        return render_template(LOGIN)

# Logout route
@app.route('/logout', methods=['GET'])
def logout():
    """ Logout the user and clean the cache session"""
    # Forget any user
    session.clear()
    return render_template(LOGIN)

# Profile route
@app.route('/profile', methods=['GET'])
def profile():
    if "user" not in session.keys() or session["user"] is None:
        return render_template(LOGIN)
    else:
        return render_template(PROFILE, user=session["user"])

# Todos route
@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if "user" not in session.keys() or session["user"] is None:
        return render_template(LOGIN)
    else:
        todos = []
        records = db.session.query(ToDo).filter(ToDo.user_id==session["user"].id).all()
        pending = 0
        completed = 0
        for record in records:
            if record.status == True:
                completed = completed + 1
            else:
                pending = pending + 1
            
            todo = {"id": record.id, "title": record.title, "status": "Completed" if record.status == 1 else "Pending"}
            todos.append(todo)
        
        return render_template(TODOS, todos=todos, pending=pending, completed=completed)

# Change todo route
@app.route('/changetodo', methods=['POST'])
def changetodo():
    todo_id = request.form.get("todo_id")
    
    todo = db.session.query(ToDo).filter(ToDo.id==todo_id).first()
    if not todo is None:
        todo.status = not todo.status
        db.session.commit()
        return "Completed" if todo.status else "Pending"
    else:
        return "ToDo not founded"

# Delete todo route
@app.route('/deletetodo', methods=['POST'])
def deletetodo():
    todo_id = request.form.get("todo_id")
    
    todo = db.session.query(ToDo).filter(ToDo.id==todo_id).first()
    if not todo is None:
        db.session.delete(todo)
        db.session.commit()
        return "ToDo deleted"
    else:
        return "ToDo not founded"

# Delete todo route
@app.route('/addtodo', methods=['POST'])
def addtodo():
    todo_title = request.form.get("todo_title")

    if todo_title:
        todo = ToDo(title=todo_title, user_id=session["user"].id)
        db.session.add(todo)
        db.session.commit()

        return jsonify({ "id": todo.id, "title": todo.title, "status": "Completed" if todo.status == 1 else "Pending" })
    else:
        return "Title is required to add a ToDo"