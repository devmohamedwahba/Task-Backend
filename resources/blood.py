from flask_restful import Resource, reqparse
import os
from werkzeug.datastructures import FileStorage
from db import db
from models.blood import BloodModel
import datetime
from utils import image_helper
from PIL import Image
import pytesseract
import random


class BloodUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "blood", location='files',
        type=FileStorage, required=True, help="this field is required"
    )

    @classmethod
    def post(cls):
        submitted_file = BloodUpload.parser.parse_args()

        if submitted_file:
            if not image_helper.is_filename_safe(submitted_file['blood']):
                return {'message': 'upload correct img'}, 404

            filename = submitted_file['blood'].filename
            file_first_name = os.path.splitext(filename)[0]
            extension = image_helper.get_extension(submitted_file['blood'])
            path = os.path.join('uploads', file_first_name + str(datetime.datetime.now()) + extension)
            submitted_file['blood'].save(path)
            img = Image.open(path)
            text = pytesseract.image_to_string(img)
            # logic of patient pressure image
            blood_text = BloodModel(patient_name=text, pressure=random.randint(0, 100))
            blood_text.save_to_db()
            return {'message': f'{text}'}

    @classmethod
    def get(cls):
        all_patient = BloodModel.find_all_patients()
        return [patient.json() for patient in all_patient]
