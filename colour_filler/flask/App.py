from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT NOT NULL
            )
        ''')
        conn.commit()


@app.route('/items', methods=['GET'])
def get_items():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = [{'id': row[0], 'name': row[1], 'value': row[2]} for row in cursor.fetchall()]
    return jsonify(items)


@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data or 'value' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, value) VALUES (?, ?)", (data['name'], data['value']))
        conn.commit()
        item_id = cursor.lastrowid

    return jsonify({'id': item_id, 'name': data['name'], 'value': data['value']}), 201


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
