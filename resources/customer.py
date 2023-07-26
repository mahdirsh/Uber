from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from db import db
from models import CustomerModel
from schemas import CustomerSchema, CustomerUpdateSchema



blp = Blueprint("Customers", __name__, description="Operation on customers.")


@blp.route("/customer/<int:customer_id>")
class Customer(MethodView):
    @jwt_required()
    @blp.response(200, CustomerSchema)
    def get(self, customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        return customer
    
    @jwt_required()
    def delete(self, customer_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilage required.")

        customer = CustomerModel.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()

        return {"message": "Customer deleted."}
    
    @blp.arguments(CustomerUpdateSchema)
    @blp.response(200, CustomerSchema)
    def put(self, customer_data, customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        if customer:
            customer.name = customer_data["name"]
            customer.phone_number = customer_data["phone_number"]
            customer.location_latitude = customer_data["location_latitude"]
            customer.location_longitude = customer_data["location_longitude"]
        else:
            customer = CustomerModel(id=customer_id, **customer_data)

        
        try:
            db.session.add(customer)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A customer with that phone number already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the customer.")

        return customer
    
@blp.route("/customer")
class CustomerList(MethodView):
    @jwt_required()
    @blp.response(200, CustomerSchema(many=True))
    def get(self):
        return CustomerModel.query.all()
    
    @jwt_required()
    @blp.arguments(CustomerSchema)
    @blp.response(201, CustomerSchema)
    def post(self, customer_data):
        customer = CustomerModel(**customer_data)

        try:
            db.session.add(customer)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A customer with that phone number already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the customer.")

        return customer
    

