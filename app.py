from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# Database connection
def get_db():
    return sqlite3.connect("database.db")

# Create tables automatically
def create_tables():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
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
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        conn.execute("INSERT INTO users (username,email,password) VALUES (?,?,?)",
                     (username,email,password))
        conn.commit()
        return redirect('/login')

    return render_template("register.html")

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                            (email,password)).fetchone()

        if user:
            session['user_id'] = user[0]
            return redirect('/')
    
    return render_template("login.html")

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
                     (title,content,user_id,datetime.now()))
        conn.commit()
        return redirect('/')

    return render_template("create.html")

# Delete Post
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    return redirect('/')

app.run(debug=True)