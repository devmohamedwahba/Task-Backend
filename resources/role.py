from flask_restful import Resource, reqparse
from models.role import RoleModel


class UserRole(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="this field is required"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        role = RoleModel(**data)
        if role.find_by_name(role.name):
            return {"message": "Role already Exists"}
        role.save_to_db()
        return {"message": "Role Created Successfully"}, 201