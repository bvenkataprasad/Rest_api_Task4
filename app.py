from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for users
users = {}  # Format: {id: {"name": ..., "email": ...}}
next_id = 1  # Auto-increment user ID


# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


# GET a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in users:
        return jsonify(users[user_id]), 200
    return jsonify({"error": "User not found"}), 404


# POST - Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    global next_id
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    users[next_id] = {
        "name": data["name"],
        "email": data["email"]
    }
    next_id += 1

    return jsonify({"message": "User added successfully", "id": next_id - 1}), 201


# PUT - Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "name" in data:
        users[user_id]["name"] = data["name"]
    if "email" in data:
        users[user_id]["email"] = data["email"]

    return jsonify({"message": "User updated successfully"}), 200


# DELETE - Remove a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
