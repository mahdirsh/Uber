from marshmallow import Schema, fields, validate


class DriverSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    car_model = fields.Str(required=True)
    car_plate_number = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    location_latitude = fields.Float(required=True)
    location_longitude = fields.Float(required=True)
    distance_to_start_location = fields.Float(dump_only=True)

    


class CustomerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    location_latitude = fields.Float(required=True)
    location_longitude = fields.Float(required=True)


class TripSchema(Schema):
    id = fields.Int(dump_only=True)
    #source = fields.Str(required=True)
    #destination = fields.Str(required=True)
    #distance = fields.Float(required=True)
    #driver_id = fields.Int(required=True, load_only=True)
    customer_id = fields.Int(required=True, load_only=True)
    start_location_latitude = fields.Float(required=True)
    start_location_longitude = fields.Float(required=True)
    end_location_latitude = fields.Float(required=True)
    end_location_longitude = fields.Float(required=True)
    status = fields.Str(required=True, validate=[validate.OneOf(["Pending", "In Progress", "Completed"])])
    nearest_drivers = fields.Nested(DriverSchema, many=True, dump_only=True)
    price = fields.Int(required=False)
    
class DriverUpdateSchema(Schema):
    name = fields.Str(required=False)
    car_model = fields.Str(required=False)
    car_plate_number = fields.Str(required=False)
    phone_number = fields.Str(required=False)
    location_latitude = fields.Float(required=False)
    location_longitude = fields.Float(required=False)


class CustomerUpdateSchema(Schema):
    name = fields.Str(required=False)
    phone_number = fields.Str(required=False)
    location_latitude = fields.Float(required=False)
    location_longitude = fields.Float(required=False)

class TripUpdateSchema(Schema):
    driver_id = fields.Int(required=False)
    customer_id = fields.Int(required=False)
    start_location_latitude = fields.Float(required=False)
    start_location_longitude = fields.Float(required=False)
    end_location_latitude = fields.Float(required=False)
    end_location_longitude = fields.Float(required=False)
    status = fields.Str(required=False)
    

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)
    #role = fields.Str(required=True)

