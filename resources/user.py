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

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        if UserModel.find_by_email(data["email"]):
            return {"message": "User Already Exist"}, 400
        if not RoleModel.find_by_id(data["role_id"]):
            return {"message": "There is no role Match"}, 400

        user = UserModel(**data)
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
