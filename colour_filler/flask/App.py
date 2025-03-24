from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entropy REAL NOT NULL,
                gamestate TEXT NOT NULL UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gamestate TEXT NOT NULL,
                playtime INTEGER NOT NULL,
                FOREIGN KEY (gamestate) REFERENCES levels(gamestate)
            )
        ''')
        conn.commit()


@app.route('/levels', methods=['GET'])
def get_levels():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM levels")
        levels = [{'id': row[0], 'entropy': row[1], 'gamestate': row[2]} for row in cursor.fetchall()]
    return jsonify(levels)


@app.route('/levels', methods=['POST'])
def add_level():
    data = request.get_json()
    if not data or 'entropy' not in data or 'gamestate' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO levels (entropy, gamestate) VALUES (?, ?)", (data['entropy'], data['gamestate']))
        conn.commit()
        level_id = cursor.lastrowid

    return jsonify({'id': level_id, 'entropy': data['entropy'], 'gamestate': data['gamestate']}), 201


@app.route('/plays', methods=['GET'])
def get_plays():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plays")
        plays = [{'id': row[0], 'gamestate': row[1], 'playtime': row[2]} for row in cursor.fetchall()]
    return jsonify(plays)


@app.route('/plays', methods=['POST'])
def add_play():
    data = request.get_json()
    if not data or 'gamestate' not in data or 'playtime' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM levels WHERE gamestate = ?", (data['gamestate'],))
        if cursor.fetchone()[0] == 0:
            return jsonify({'error': 'Gamestate not found in levels'}), 400

        cursor.execute("INSERT INTO plays (gamestate, playtime) VALUES (?, ?)", (data['gamestate'], data['playtime']))
        conn.commit()
        play_id = cursor.lastrowid

    return jsonify({'id': play_id, 'gamestate': data['gamestate'], 'playtime': data['playtime']}), 201


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
