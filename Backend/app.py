import sys
sys.path.insert(0, '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src')

from face_capture import face_capture 
from waga import testRecognize 


from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, joinedload,Mapped, mapped_column
from sqlalchemy import Integer, String, select
from werkzeug.security import generate_password_hash, check_password_hash

from models import Users, db , tokenBlacklist #Users class 

api = Flask(__name__)
CORS(api, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing
api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
api.config['SECRET_KEY'] = 'your_secret_key_here'
api.config['JWT_SECRET_KEY'] = 'jwt_secret_key_here'

db.init_app(api)
jwt= JWTManager(api)


@api.route('/test')
def test():
    return 'test'

@api.route('/registerAdmin', methods=['POST'])
def registerAdmin():
    data = request.get_json()
    if not data or not data.get('Email') or not data.get('Password'):
        return jsonify({"msg": "Missing email or password"}), 400

    Email = data['Email']
    password= data['Password']

    if Users.query.filter_by(Email=Email).first() is not None:
        return jsonify({"msg": "User already exists"}), 409

    pwd_hash = generate_password_hash(password)
    new_Admin = Users(Email=Email, Password=pwd_hash, Active=True, Role="Admin")
    db.session.add(new_Admin)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@api.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        Email = data['Email']
        password = data['Password']

        user = Users.query.filter_by(Email=Email).first() or Users.query.filter_by(Role="Admin", Email=Email).first()
        
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

        acc_token = create_access_token(identity={'email': Email, 'role': user.Role})
        return jsonify({'acc_token': acc_token}), 200
    return "waga"

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('Email') or not data.get('Password'):
        return jsonify({"msg": "Missing email or password"}), 400

    Email = data['Email']
    password= data['Password']
    username = data['username']

    if Users.query.filter_by(Email=Email).first() is not None:
        return jsonify({"msg": "User already exists"}), 409

    pwd_hash = generate_password_hash(password)
    new_user = Users(Email=Email, Password=pwd_hash, Active=True, Role="client")
    db.session.add(new_user)
    db.session.commit()

    face_capture(username)

    return jsonify({"msg": "User registered successfully"}), 201


@api.route('/testLogin', methods=['POST'])
def testLogin():
    testRecognize()

if __name__ == '__main__':
    with api.app_context():
        db.create_all()
    api.run(debug=True,  port=5000)