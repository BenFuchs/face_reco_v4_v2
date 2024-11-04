import sys
sys.path.insert(0, '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src')
import datetime
from face_capture import face_capture #vscode issue the import works
from waga import testRecognize #vscode issue the import works

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, joinedload,Mapped, mapped_column
from sqlalchemy import Integer, String, select
from werkzeug.security import generate_password_hash, check_password_hash

from models import Users, db , userInOrOut , RecognitionLog

api = Flask(__name__)
CORS(api, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing
api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
api.config['SECRET_KEY'] = 'your_secret_key_here'
api.config['JWT_SECRET_KEY'] = 'jwt_secret_key_here'

db.init_app(api)
jwt= JWTManager(api)


@api.route('/test')
def test():
    print('test')
    return 'test'

@api.route('/registerAdmin', methods=['POST'])
def registerAdmin():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('Password'):
        return jsonify({"msg": "Missing email or password"}), 400

    email = data['email']
    password= data['Password']

    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "User already exists"}), 409

    pwd_hash = generate_password_hash(password)
    new_Admin = Users(email=email, password=pwd_hash, active=True, role="Admin")
    db.session.add(new_Admin)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@api.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['Password']

        user = Users.query.filter_by(email=email).first() or Users.query.filter_by(Role="Admin", email=email).first()
        
        if not user:
            return jsonify({
                'message': 'User not found'
            }), 401

        if user.Active == 0:
            return jsonify({"msg": "User has been set to inactive by admin"}), 403

        if not check_password_hash(user.Password, password):
            return jsonify({
                'message': 'Wrong password'
            }), 401

        acc_token = create_access_token(identity={'email': email, 'role': user.role})
        return jsonify({'acc_token': acc_token}), 200
    return "waga"

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Missing email or password"}), 400

    email = data['email']
    password= data['password']
    username = data['username']

    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "User already exists"}), 409

    pwd_hash = generate_password_hash(password)
    new_user = Users(email=email, password=pwd_hash, username=username ,active=True, role="client")
    db.session.add(new_user)
    db.session.commit()

    face_capture(username)

    return jsonify({"msg": "User registered successfully"}), 201

@api.route('/recognize_user', methods=['POST'])
def recognize_user():
    data = request.get_json()
    username = data.get('user_id')
    
    if not username:
        return jsonify({"error": "User ID is required"}), 400
    
    # Check if the user already has a record in userInOrOut
    user_entry = db.session.execute(
        select(userInOrOut).filter_by(user_id=username)
    ).scalar_one_or_none()
    
    current_time = datetime.now()
    
    if user_entry is None:
        # Create a new userInOrOut entry with the latest time
        new_entry = userInOrOut(user_id=username, flag=True, time=current_time)
        db.session.add(new_entry)
    else:
        # Update the time for an existing entry
        user_entry.time = current_time #log new time entry 
        user_entry.flag = not user_entry.flag  # toggle flag switch 

    # Log every recognition in the RecognitionLog table
    new_log_entry = RecognitionLog(user_id=username, recognition_time=current_time)
    db.session.add(new_log_entry)
    
    db.session.commit()  # Commit all changes to the database
    
    return jsonify({"message": "User recognized and logged", "user_id": username, "time": current_time}), 201


if __name__ == '__main__':
    with api.app_context():
        db.create_all()
    api.run(debug=True,  port=5000)