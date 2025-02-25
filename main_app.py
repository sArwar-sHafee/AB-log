from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import base64
import markdown
import json
from flask import jsonify
from datetime import timedelta

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'e4f3b2d1a9c8e7f60123456789abcdef0123456789abcdef0123456789abcdef'  # Change this for production

DATABASE = 'posts.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    conn = get_db_connection()
    # Create posts table with an "images" field that stores a JSON array (as TEXT)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            content TEXT NOT NULL,
            images TEXT,
            username TEXT NOT NULL,
            likes INTEGER DEFAULT 0
        )
    ''')
    # Create users table.
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database.
init_db()

# Jinja filter to convert Markdown to HTML.
@app.template_filter('markdown')
def markdown_filter(text):
    return markdown.markdown(text)

# Jinja filter to convert a JSON string into a Python list.
@app.template_filter('fromjson')
def fromjson_filter(s):
    if s:
        try:
            return json.loads(s)
        except Exception:
            return []
    return []

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    # Only allow access if the user is logged in.
    if 'username' not in session:
        flash("You need to log in to create a post.")
        return redirect(url_for('login', next=url_for('create')))
    
    if request.method == 'POST':
        content = request.form.get('content')
        # Process multiple images.
        image_files = request.files.getlist('image')
        images = []
        for image_file in image_files:
            if image_file and image_file.filename != '':
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                image_data = f"data:{image_file.content_type};base64,{image_data}"
                images.append(image_data)
        images_json = json.dumps(images) if images else None

        timestamp = datetime.now().strftime('%d-%m-%Y ')
        username = session['username']
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO posts (timestamp, content, images, username) VALUES (?, ?, ?, ?)',
            (timestamp, content, images_json, username)
        )
        conn.commit()
        conn.close()
        flash("Post created successfully!")
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    conn = get_db_connection()
    conn.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    if 'username' not in session:
        flash("You must be logged in to delete a post.")
        return redirect(url_for('login'))
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post is None:
        flash("Post not found.")
    elif session.get('username') != post['username']:
        flash("You can only delete your own posts.")
    else:
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        flash("Post deleted successfully!")
    conn.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Capture the "next" parameter if provided.
    next_page = request.args.get('next')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session.permanent = True  # Make the session persistent
            flash("Logged in successfully!")
            # Get the "next" destination from the hidden field.
            next_dest = request.form.get('next')
            # If next_dest is empty or "None", default to home.
            if not next_dest or next_dest == "None":
                next_dest = url_for('index')
            return redirect(next_dest)
        else:
            flash("Invalid credentials, please try again.")
    return render_template('login.html', next=next_page)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()
            flash("Registration successful! You can now log in.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose another.")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!")
    return redirect(url_for('index'))

@app.route('/load_posts')
def load_posts():
    # Get the offset (default to 0) from the query parameters.
    offset = request.args.get('offset', 0, type=int)
    limit = 10  # Number of posts per batch
    conn = get_db_connection()
    posts = conn.execute(
        'SELECT * FROM posts ORDER BY id DESC LIMIT ? OFFSET ?', (limit, offset)
    ).fetchall()
    conn.close()

    # Convert the posts to a list of dictionaries
    posts_list = []
    for post in posts:
        posts_list.append({
            'id': post['id'],
            'timestamp': post['timestamp'],
            'content': post['content'],
            'images': post['images'],  # This is stored as JSON in the DB
            'username': post['username'],
            'likes': post['likes']
        })
    return jsonify(posts_list)


if __name__ == '__main__':
    app.permanent_session_lifetime = timedelta(days=30)
    app.run(debug=False)