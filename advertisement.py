from flask import Flask,render_template,request,redirect,url_for, g
import sqlite3
# comment

app = Flask(__name__, template_folder='templates')

app.config['DATABASE'] = 'ads.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM advertisements")
    advertisements = cursor.fetchall()
    cursor.close()
    return render_template('advertisement.html', advertisements=advertisements)

@app.route('/add', methods=['POST'])
def add_advertisement():
    conn = get_db()
    cursor = conn.cursor()
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    price = request.form['price']
    cursor.execute("INSERT INTO advertisements (title, description, status, price) VALUES (?, ?, ?, ?)", (title, description, status, price))
    conn.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit_advertisement():
    conn = get_db()
    cursor = conn.cursor()
    advertisement_id = request.form['id']
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    price = request.form['price']
    cursor.execute("UPDATE advertisements SET title = ?, description = ?, status = ?, price = ? WHERE id = ?", (title, description, status, price, advertisement_id))
    conn.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_advertisement():
    conn = get_db()
    cursor = conn.cursor()
    advertisement_id = request.form['id']
    cursor.execute("DELETE FROM advertisements WHERE id = ?", (advertisement_id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
