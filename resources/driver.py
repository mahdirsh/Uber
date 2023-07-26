from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import DriverModel
from schemas import DriverSchema, DriverUpdateSchema


blp = Blueprint("drivers", __name__, description= "Operation on drivers.")



@blp.route("/driver/<string:driver_id>")
class Driver(MethodView):
    @jwt_required()
    @blp.response(200, DriverSchema)
    def get(self, driver_id):
        driver = DriverModel.query.get_or_404(driver_id)
        return driver


    @jwt_required()
    def delete(self, driver_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilage required.")

        driver = DriverModel.query.get_or_404(driver_id)
        db.session.delete(driver)
        db.session.commit()

        return {"message": "Driver deleted."}


    @blp.arguments(DriverUpdateSchema)
    @blp.response(200, DriverSchema)
    def put(self, driver_data, driver_id):
        driver = DriverModel.query.get_or_404(driver_id)
        if driver:
            driver.name = driver_data["name"]
            driver.car_model = driver_data["car_model"]
            driver.car_plate_number = driver_data["car_plate_number"]
            driver.phone_number = driver_data["phone_number"]
            driver.location_latitude = driver_data["location_latitude"]
            driver.location_longitude = driver_data["location_longitude"]
        else:
            driver = DriverModel(id=driver_id, **driver_data)

        try:
            db.session.add(driver)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A driver with that phone number or car plate already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the driver.")

        return driver

        

@blp.route("/driver")
class DriverList(MethodView):
    @jwt_required()
    @blp.response(200, DriverSchema(many=True))
    def get(self):
        return DriverModel.query.all()


    @jwt_required()
    @blp.arguments(DriverSchema)
    @blp.response(201, DriverSchema)
    def post(self, driver_data):
        driver = DriverModel(**driver_data)

        try:
            db.session.add(driver)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A driver with that phone number or car plate already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the driver.")

        return driver
