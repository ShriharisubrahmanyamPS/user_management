from flask import Flask,request,jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__)


bcrypt = Bcrypt()

users = {}


@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users:
        return jsonify({'message': 'Username already exists!'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users[username] = hashed_password
    
    return jsonify({'message': 'User added successfully.'}), 201


@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    if username in users:
        del users[username]
        return jsonify({'message': 'User deleted successfully.'}), 200
    return jsonify({'message': 'User not found.'}), 404


@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users and bcrypt.check_password_hash(users[username], password):
        return jsonify({'message': 'Authentication successful.'}), 200
    
    return jsonify({'message': 'Authentication failed.'}), 401

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
