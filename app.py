from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, UserLogout
from resources.role import UserRole
from resources.blood import BloodUpload


app = Flask(__name__)
app.secret_key = "you will never guess password"
app.config.from_object("config")

CORS(app)

api = Api(app)

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.init_app(app=app)
    db.create_all(app=app)
    doctor = RoleModel.find_by_name('doctor')
    if not doctor:
        role_doctor = RoleModel(name='doctor')
        role_doctor.save_to_db()
    patient = RoleModel.find_by_name('patient')
    if not patient:
        role_patient = RoleModel(name='patient')
        role_patient.save_to_db()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
            decrypted_token["jti"] in BLACKLIST
    )


"""  User Api """
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserRole, "/role")
api.add_resource(BloodUpload, "/blood")

from models.role import RoleModel
from models.user import UserModel
from models.blood import BloodModel

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
