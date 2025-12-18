from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# In-memory database
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    {"id": 4, "name": "David", "email": "david@example.com"},
    {"id": 5, "name": "Eve", "email": "eve@example.com"}
]

@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    parameters:
      - name: page
        in: query
        type: integer
        description: Page number
        default: 1
      - name: limit
        in: query
        type: integer
        description: Items per page
        default: 10
      - name: name
        in: query
        type: string
        description: Filter by name
    responses:
      200:
        description: List of users
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
            total:
              type: integer
            page:
              type: integer
            limit:
              type: integer
    """
    # Filtering
    name_filter = request.args.get('name')
    filtered_users = users
    if name_filter:
        filtered_users = [u for u in users if name_filter.lower() in u['name'].lower()]

    # Pagination
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    start = (page - 1) * limit
    end = start + limit
    
    paginated_users = filtered_users[start:end]
    
    return jsonify({
        "data": paginated_users,
        "total": len(filtered_users),
        "page": page,
        "limit": limit
    })

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a single user
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User found
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
      404:
        description: User not found
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      201:
        description: User created
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
      400:
        description: Invalid data
    """
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_user = {
        "id": users[-1]['id'] + 1 if users else 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a user
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      200:
        description: User updated
      404:
        description: User not found
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user.update(data)
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User deleted
    """
    global users
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": "User deleted"}), 200

# --- New Endpoints ---

@app.route('/login', methods=['POST'])
def login():
    """
    Login to get a token
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              default: admin
            password:
              type: string
              default: password
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            token:
              type: string
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    if data and data.get('username') == 'admin' and data.get('password') == 'password':
        return jsonify({"token": "fake-jwt-token-123456"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
def protected():
    """
    Access protected resource
    ---
    tags:
      - Auth
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer <token>
    responses:
      200:
        description: Access granted
      401:
        description: Unauthorized
    """
    auth_header = request.headers.get('Authorization')
    if auth_header == "Bearer fake-jwt-token-123456":
        return jsonify({"message": "Access granted to protected resource", "secret_data": "42"}), 200
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
