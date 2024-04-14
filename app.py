from flask import Flask
from user_function import routes
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:todo-admin@todo.ckgbjrurodq3.ap-south-1.rds.amazonaws.com:3306/to_do_app'  # Replace 'your_database_uri' with your actual URI
db.init_app(app)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
