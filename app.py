from flask import Flask, jsonify, request
import mysql.connector 
from dotenv import load_dotenv 
import os

app = Flask(__name__)
load_dotenv()

def get_db_connection(): 
    conn = mysql.connector.connect( 
        host=os.getenv("DB_HOST"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASS"), 
        database=os.getenv("DB_NAME") 
    ) 
    return conn

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the simple API!",
        "status": "success"
    })

@app.route('/users')
def users():
    data = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"}
    ]
    return jsonify(data)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM users_id WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route('/user/add', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    favorites = data.get('Favorites', None)
    mdp = data.get('mdp')
    email = data.get('EMAIL', None)
    editor_pick = data.get('Editor_Pick', '')
    if not name or not mdp:
        return jsonify({"error": "name and mdp are required"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users_id (name, Favorites, mdp, EMAIL, Editor_Pick) VALUES (%s, %s, %s, %s, %s)",
            (name, favorites, mdp, email, editor_pick)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({
            "success": True,
            "id": user_id,
            "name": name,
            "Favorites": favorites,
            "EMAIL": email,
            "Editor_Pick": editor_pick
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)