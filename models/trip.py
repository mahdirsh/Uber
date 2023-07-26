from db import db


class TripModel(db.Model):
    __tablename__ = "trips"


    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    start_location_latitude = db.Column(db.Float, nullable=False)
    start_location_longitude = db.Column(db.Float, nullable=False)
    end_location_latitude = db.Column(db.Float, nullable=False)
    end_location_longitude = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=True)
    
  