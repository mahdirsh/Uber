from db import db


class DriverModel(db.Model):
    __tablename__ = "drivers"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    car_model = db.Column(db.String(80), nullable=False)
    car_plate_number = db.Column(db.String(80), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    location_latitude = db.Column(db.Float, nullable=False)
    location_longitude = db.Column(db.Float, nullable=False)
    distance_to_start_location = db.Column(db.Float, nullable=True)

    