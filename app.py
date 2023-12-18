from flask import g, Flask, render_template, request, redirect, url_for, flash,abort
from werkzeug.wrappers import Response as FlaskResponse
from werkzeug.wrappers import Request as FlaskRequest   
import sqlite3
app = Flask(__name__)
app.secret_key = 'kibo'

DATABASE = 'tasks.db'

def get_db():
        conn = sqlite3.connect(DATABASE)
        return conn

def create_table():
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task_name TEXT NOT NULL,
                task_description TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

create_table()

@app.route('/', methods=['GET', 'POST'])

def user(): 
    error = None  # Initialize the error variable
    if request.method =="POST":
           username = request.form["username"]
           print(f"hello {username}")
           try:
                with get_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
                    conn.commit()
                flash(f'User {username} created successfully!', 'success')
                return redirect(url_for('home', username=username))
           except sqlite3.IntegrityError:
                error = f"User '{username}' already exists. Please choose a different username."
                flash(error, 'error')
    return render_template("user.html", error=error)

@app.route('/<username>', methods = ['GET'])
def home(username):
      return render_template('home.html', username =username )

@app.route('/users', methods = ['GET'])
def users():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
    return render_template('users.html', users=users) 
