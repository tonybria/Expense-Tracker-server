import json
from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import jwt_required, create_access_token, unset_jwt_cookies, get_jwt, get_jwt_identity,  JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import User, Expense, db

app = Flask(__name__)

# Configure your database connection
app.config['SECRET_KEY'] = 'ricktheruler-nyc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # Use app.json_encoder.compact

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_TRACK_ECHO = True

CORS(app)
bcrypt = Bcrypt(app)
db.init_app(app)

# with app.app_context():
#     db.create_all()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

@app.route("/")
def hello_world():
    return "<p>Hello Mars!</p>"

@app.route("/login", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Wrong email or passowrd"})
   
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized access"})
    
    access_token = create_access_token(identity=email)
    
    return jsonify({
        "email":email,
        "access_token": access_token
    })
    
@app.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email")
    password = request.json.get("password")

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "Email already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')    
    new_user = User(username="musk", email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id":new_user.id,
        "email": new_user.email
    })

@app.after_request
def refresh_expiring_jwt(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data=response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    
    except (RuntimeError, KeyError):
        return response

@app.route('/logout', methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route('/profile/<getemail>')
@jwt_required()
def my_profile(getemail):
    print(getemail);
    if not getemail:
        return jsonify({"error": "Unauthorized Access"}), 401
    
    user = User.query.filter_by(email=getemail).first()

    response_body = {
        "id": user.id,
        "username":user.username,
        "email":user.email
    }

    return response_body



@app.route("/<string:username>/expenses", methods=["GET", "POST"])
def expenses(username):
    if request.method == "GET":
        user = User.query.filter_by(username=username).first()
        if not user:
            response = make_response(
                jsonify({'message': 'User not found'}), 404
            )
            return response
        else:
            expenses = Expense.query.filter_by(user_id=user.id).all()
            expense_list = []
            for expense in expenses:
                expense_dict = {
                    "id": expense.id,
                    "name": expense.name,
                    "amount": expense.amount,
                    "date": expense.date.isoformat(),
                    "category": expense.category.name
                }
                expense_list.append(expense_dict)
            response = make_response(
                jsonify(expense_list), 200
            )
            return response


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
