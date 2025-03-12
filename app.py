from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    short_url = generate_short_url()

    conn = get_db_connection()
    conn.execute('INSERT INTO urls (short, original) VALUES (?, ?)', (short_url, original_url))
    conn.commit()
    conn.close()

    return f'Short URL: <a href="/{short_url}">{request.host}/{short_url}</a>'


@app.route('/<short_url>')
def redirect_to_original(short_url):
    conn = get_db_connection()
    url_entry = conn.execute('SELECT original FROM urls WHERE short = ?', (short_url,)).fetchone()
    conn.close()

    if url_entry:
        return redirect(url_entry['original'])
    else:
        return 'URL not found', 404


if __name__ == '__main__':
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    short TEXT UNIQUE,
                    original TEXT)''')
    conn.commit()
    conn.close()

    app.run(debug=True)
