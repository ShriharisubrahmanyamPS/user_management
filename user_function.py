# todos.py

from datetime import datetime
from models import Users
from flask import Blueprint, jsonify, request
from database import create_connection
# from auth import authenticate_token
from database import db
from flask_bcrypt import Bcrypt
import app
from auth import authenticate_token

routes = Blueprint('user_function', __name__)

bcrypt = Bcrypt()

@routes.route('/adduser', methods=['POST'])
def add_user():  
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    token = token.split(" ")[1] if token.startswith("Bearer ") else None
    if not token:
        return jsonify({'error': 'Invalid token format'}), 401
    if not authenticate_token(token):
        return jsonify({'error': 'Invalid token'}), 401
    try:
        conn=create_connection()
        cur=conn.cursor()
        users="SELECT id, username, password, createdAt, updatedAt FROM to_do_app.Users"
        cur.execute(users)
        users_data=cur.fetchall()
        for user in users_data:
            if username in user[1]:
                return jsonify({'message': 'Username already exists!'}), 400
        insert_query_user="INSERT INTO to_do_app.Users (username, password, createdAt, updatedAt) VALUES(%s, %s, %s, %s);"
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute(insert_query_user,(username,str(hashed_password),datetime.now(),datetime.now()))
        user_id= cur.lastrowid
        print('user_id',user_id)
        conn.commit()
        roles="SELECT role_id, `role` FROM to_do_app.roles where role = %s;"
        cur.execute(roles,(str(role)))
        role_id=roles[0]
        print('role_id',role_id)
        insert_query_role="INSERT INTO to_do_app.user_roles (user_id, role_id) VALUES(%s, %s);"
        cur.execute(insert_query_role,(user_id,role_id))
        conn.commit()
        cur.close() 
    except Exception as e:
        print(e)
        conn.rollback()
        cur.close()      
    return jsonify({'message': 'User added successfully.'}), 201


@routes.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    conn=create_connection()
    cur=conn.cursor()
    users="SELECT id, username, password, createdAt, updatedAt FROM to_do_app.Users"
    cur.execute(users)
    users_data=cur.fetchall()
    for user in users_data:
        if username in user[1]:
           user_delete="delete from to_do_app.Users where username=%s"
           cur.execute(users_data,(username))
           conn.commit()
           return jsonify({'message': 'User Deleted'}), 404          

    return jsonify({'message': 'User not found.'}), 404


@routes.route('/getuser', methods=['GET'])
def get_user(): 
    try: 
        print(create_connection())
        conn=create_connection()
        cur=conn.cursor()
        users="SELECT id, username, password, createdAt, updatedAt FROM to_do_app.Users"
        cur.execute(users)
        users_data=cur.fetchall()
        print(users_data)
        users=Users.query.all()
        print(users)
    except Exception as e:
        print(e)
    return jsonify(users_data)

