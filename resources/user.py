from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from models.user import UserModel
from models.role import RoleModel
from blacklist import BLACKLIST
from werkzeug.security import check_password_hash
from validate_email import validate_email
import requests
import json

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "email", type=str, required=True, help="this field is required"
)
_user_parser.add_argument(
    "password", type=str, required=True, help="password cant be blank"
)


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="userName cant be blank"
    )
    parser.add_argument(
        "email", type=str, required=True, help="email is required"
    )
    parser.add_argument(
        "password", type=str, required=True, help="password can not be blank"
    )

    parser.add_argument(
        "role_id", type=int, required=True, help="role_id field can not be blank"
    )
    parser.add_argument(
        "captcha", type=str, required=True, help="captcha field can not be blank"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        if not validate_email(data["email"]):
            return {"message": "Email is invalid"}, 400
        if UserModel.find_by_email(data["email"]):
            return {"message": "User Already Exist"}, 400
        if not RoleModel.find_by_id(data["role_id"]):
            return {"message": "There is no role Match"}, 400
        captcha_token = data['captcha']
        cap_url = 'https://www.google.com/recaptcha/api/siteverify'
        cap_secret = '6LdepUwaAAAAAMpgIoRBiwGUNCuXA26OS8hqDoYP'
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success'] == False:
            return {"message": "Some thing wrong "}, 404

        user = UserModel(username=data['username'], email=data['email'], password=data['password'],
                         role_id=data['role_id'])
        user.save_to_db()

        return {"message": "User Created Successfully"}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, expires_delta=False, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token,
                       "role": user.role.json()
                   }, 200

        return {"message": "Email Or Password Invalid"}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": "User Logout Successfully".format(user_id)}, 200
