from db import db


class BloodModel(db.Model):
    __tablename__ = "bloods"
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100))
    pressure = db.Column(db.Integer)

    def __repr__(self):
        return f'this is {self.patient_name}'

    def json(self):
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "pressure": self.pressure
        }

    @classmethod
    def find_all_patients(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
