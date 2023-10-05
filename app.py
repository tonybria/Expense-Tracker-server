from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import User, Expense, db

app = Flask(__name__)

# Configure your database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # Use app.json_encoder.compact

CORS(app)
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

@app.route("/<string:username>/expenses", methods=["GET", "POST"])  # Fixed the route definition
def expenses(username):
    if request.method == "GET":
        user = User.query.filter_by(username=username).first()  # Fixed filter_by
        if not user:
            response = make_response(
                jsonify({'message': 'User not found'}), 404
            )
            return response
        else:
            expenses = Expense.query.filter_by(user_id=user.id).all()  # Fixed filter_by
            expense_list = []
            for expense in expenses:
                expense_dict = {
                    "id": expense.id,
                    "name": expense.name,
                    "amount": expense.amount,
                    "date": expense.date.isoformat(),  # Added () to isoformat
                    "category": expense.category.name
                }
                expense_list.append(expense_dict)
            response = make_response(
                jsonify(expense_list), 200
            )
            return response

if __name__ == '__main__':
    app.run(debug=True)
