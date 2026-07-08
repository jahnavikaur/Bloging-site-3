from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="statics")
app.secret_key = "secret123"

# Database connection
def get_db():
    return sqlite3.connect("database.db")

# Create tables automatically
def create_tables():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    email TEXT,
                    password TEXT)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS posts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    content TEXT,
                    user_id INTEGER,
                    date TEXT)''')
    conn.commit()

create_tables()

# Home Page
@app.route('/')
def home():
    conn = get_db()
    posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    return render_template("home.html", posts=posts)

# Register
@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username,password) VALUES (?,?)",
                         (username,hashed_password))
            conn.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            error = "That username is already taken. Please choose another."

    return render_template("register.html", error=error)

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?",
                            (username,)).fetchone()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect('/')
        else:
            error = "Incorrect username or password."

    return render_template("login.html", error=error)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Create Post
@app.route('/create', methods=['GET','POST'])
def create():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']

        conn = get_db()
        conn.execute("INSERT INTO posts (title,content,user_id,date) VALUES (?,?,?,?)",
                     (title,content,user_id,datetime.now().strftime('%b %d, %Y · %I:%M %p')))
        conn.commit()
        return redirect('/')

    return render_template("create.html")

# Edit Post
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    post = conn.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()

    if post is None:
        return redirect('/')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn.execute("UPDATE posts SET title=?, content=?, date=? WHERE id=?",
                     (title,content,datetime.now().strftime('%b %d, %Y · %I:%M %p'),id))
        conn.commit()
        return redirect('/')

    return render_template("edit.html", post=post)

# Delete Post
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    return redirect('/')

app.run(debug=True)