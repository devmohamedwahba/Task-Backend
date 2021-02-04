from db import db


class RoleModel(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    users = db.relationship('UserModel', lazy="dynamic", backref="role_name")

    def __repr__(self):
        return f'this is {self.name}'

    def json(self):
        return {"id": self.id,
                "name": self.name}

    @classmethod
    def find_all_roles(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
