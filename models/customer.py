from db import db


class CustomerModel(db.Model):
    __tablename__ = "customers"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    location_latitude = db.Column(db.Float, nullable=False)
    location_longitude = db.Column(db.Float, nullable=False)
    