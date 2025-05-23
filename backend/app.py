from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

load_dotenv()
app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/api/notes', methods=['GET'])
def get_notes():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(notes)

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE id = %s", [note_id])
    note = cursor.fetchone()
    cursor.close()
    conn.close()

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify(note)

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.json
    required_fields = ['title', 'content', 'subject']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields (title, content, subject)'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content, subject, is_important) VALUES (%s, %s, %s, %s)",
            [data['title'], data['content'], data['subject'], data.get('is_important', False)]
        )
        conn.commit()
        note_id = cursor.lastrowid
        cursor.close()

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notes WHERE id = %s", [note_id])
        new_note = cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify(new_note), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        updates = []
        values = []

        for field in ['title', 'content', 'subject', 'is_important']:
            if field in data:
                updates.append(f"{field} = %s")
                values.append(data[field])

        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400

        values.append(note_id)
        query = f"UPDATE notes SET {', '.join(updates)} WHERE id = %s"

        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Note not found'}), 404

        cursor.close()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notes WHERE id = %s", [note_id])
        updated_note = cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify(updated_note), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = %s", [note_id])
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Note not found'}), 404

        cursor.close()
        conn.close()
        return jsonify({'message': 'Note deleted successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>/important', methods=['PATCH'])
def mark_important(note_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE notes SET is_important = TRUE WHERE id = %s", [note_id])
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Note not found'}), 404

        cursor.close()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notes WHERE id = %s", [note_id])
        updated_note = cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify(updated_note), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
