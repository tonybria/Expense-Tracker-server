from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from models import Expense, db

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)

migrate = Migrate(app, db)


api = Api(app)

if __name__ == '__main__':
    with app.app_context():
        
        db.create_all()
    app.run(port=5555, debug=True)
