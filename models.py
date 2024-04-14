from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    _tablename_ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    createdAt=db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt=db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Role(db.Model):
    _tablename_ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(80), unique=True)

class UserRole(db.Model):
    _tablename_ = 'user_roles'
    user_role_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))

#define a table to store the to-do list
class TodoList(db.Model):   
    _tablename_ = 'todo_list'
    todo_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.user_id'))
    todo_description = db.Column(db.String(255))
    created_on=db.Column(db.DateTime, default=datetime.utcnow)
    updated_on=db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20))
    priority = db.Column(db.String(20))
    due_date = db.Column(db.DateTime)

