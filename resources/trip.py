
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from geopy.distance import geodesic

from db import db
from models import TripModel, DriverModel
from schemas import TripSchema, TripUpdateSchema
from helpers import find_nearest_drivers





blp = Blueprint("Trips", __name__, description= "Operation on trips")


@blp.route("/trip/<int:trip_id>")
class Trip(MethodView):
    @jwt_required()
    @blp.response(200, TripSchema)
    def get(self, trip_id):
        trip = TripModel.query.get_or_404(trip_id)
       
        start_location = (trip.start_location_latitude, trip.start_location_longitude)
        end_location = (trip.end_location_latitude, trip.end_location_longitude)

        
        distance = geodesic(start_location, end_location).m

       
        price = distance * 0.1

        customer_location = (trip.start_location_latitude, trip.start_location_longitude)
        drivers = DriverModel.query.all()
        nearest_drivers = find_nearest_drivers(customer_location, drivers)

       
        response_data = {
            "id": trip.id,
            "start_location_latitude": trip.start_location_latitude,
            "start_location_longitude": trip.start_location_longitude,
            "end_location_latitude": trip.end_location_latitude,
            "end_location_longitude": trip.end_location_longitude,
            "status": trip.status,
            "price": price,
            "nearest_drivers": nearest_drivers
        }

        return response_data


    @jwt_required()
    def delete(self, trip_id):
        trip = TripModel.query.get_or_404(trip_id)
        db.session.delete(trip)
        db.session.commit()
        return {"message": "Trip deleted."}

    @blp.arguments(TripUpdateSchema)
    @blp.response(200, TripSchema)
    def put(self, trip_data, trip_id):
        trip = TripModel.query.get_or_404(trip_id)
        if trip:
            trip.driver_id = trip_data["driver_id"]
            trip.customer_id = trip_data["customer_id"]
            trip.start_location_latitude = trip_data["start_location_latitude"]
            trip.start_location_longitude = trip_data["start_location_longitude"]
            trip.end_location_latitude = trip_data["end_location_latitude"]
            trip.end_location_longitude = trip_data["end_location_longitude"]
            trip.status = trip_data["status"]
        else:
            trip = TripModel(id=trip_id, **trip_data)
            
        try:
            db.session.add(trip)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the trip.")

        return trip


@blp.route("/trip")
class TripList(MethodView):
    @jwt_required()
    @blp.response(200, TripSchema(many=True))
    def get(self):
        trips = TripModel.query.all()
        response_data = []

        for trip in trips:
            
            start_location = (trip.start_location_latitude, trip.start_location_longitude)
            end_location = (trip.end_location_latitude, trip.end_location_longitude)

            
            distance = geodesic(start_location, end_location).m

            
            price = distance * 0.1

            customer_location = (trip.start_location_latitude, trip.start_location_longitude)
            drivers = DriverModel.query.all()
            nearest_drivers = find_nearest_drivers(customer_location, drivers)

            
            trip_data = {
                "id": trip.id,
                "start_location_latitude": trip.start_location_latitude,
                "start_location_longitude": trip.start_location_longitude,
                "end_location_latitude": trip.end_location_latitude,
                "end_location_longitude": trip.end_location_longitude,
                "status": trip.status,
                "price": price,
                "nearest_drivers": nearest_drivers
            }

            response_data.append(trip_data)

        return response_data



    @jwt_required()
    @blp.arguments(TripSchema)
    @blp.response(201, TripSchema)
    def post(self, trip_data):
        trip = TripModel(**trip_data)

        start_location = (trip_data["start_location_latitude"], trip_data["start_location_longitude"])
        end_location = (trip_data["end_location_latitude"], trip_data["end_location_longitude"])

        
        distance = geodesic(start_location, end_location).m

        
        price = distance * 0.1

        
        try:
            db.session.add(trip)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An error occurred while creating the trip.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the trip.")


        customer_location = (trip.start_location_latitude, trip.start_location_longitude)
        drivers = DriverModel.query.all()
        nearest_drivers = find_nearest_drivers(customer_location, drivers)

        return {**trip_data, "nearest_drivers": nearest_drivers, "price": price}, 201

