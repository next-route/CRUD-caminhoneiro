from flask import Flask, Response, app, request
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12@localhost:3306/driver'
db = SQLAlchemy(app)

class TruckDriver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    def to_json(self):
        return{"Id": self.id, "Name": self.name, "Age": self.age, "Email": self.email}

@app.route("/truckDriver", methods=['GET'])
def get_trucksDriver():
    truckDrivers_object = TruckDriver.query.all()
    truckDrivers_json = [truckDriver.to_json() for truckDriver in truckDrivers_object]
    return generate_response(200, "Truck Drivers", truckDrivers_json)

def generate_response(status, content_name, content, message=False):
    body = {}
    body[content_name] = content
    if(message):
        body["message"] = message
    return Response(json.dumps(body), status=status, mimetype="application/json")

@app.route("/truckDriver/<id>", methods=['GET'])
def get_truckDriver(id):
    truckDriver_object = TruckDriver.query.filter_by(id=id).first()
    truckDriver_json = truckDriver_object.to_json()
    return generate_response(200, "truck", truckDriver_json)

@app.route("/truckDriver", methods=["POST"])
def create_truckDriver():
    body = request.get_json()
    try:
        truckdriver = TruckDriver(
            name=body["name"], age=body["age"], email=body["email"])
        db.session.add(truckdriver)
        db.session.commit()
        return generate_response(201, "Truck Driver", truckdriver.to_json(), "Truck Driver created with success.")
    except Exception as e:
        print('Error', e)
        return generate_response(400, "Truck Driver", {}, "Error creating Truck Driver")

@app.route("/truckDriver/<id>", methods=["PUT"])
def update_truckDriver(id):
    truckDriver_object = TruckDriver.query.filter_by(id=id).first()
    body = request.get_json()
    try:
        if("name" in body):
            truckDriver_object.name = body["name"]
        if("age" in body):
            truckDriver_object.age = body["age"]
        if("email" in body):
            truckDriver_object.email = body["email"]
        db.session.add(truckDriver_object)
        db.session.commit()
        return generate_response(200, "Truck Driver", truckDriver_object.to_json(), "Truck Driver updated with success")
    except Exception as e:
        print('Error', e)
        return generate_response(400, "Truck Driver", {}, "Error updating Truck Driver")

@app.route("/truckDriver/<id>", methods=["DELETE"])
def delete_truckDriver(id):
    truckDriver_object = TruckDriver.query.filter_by(id=id).first()
    try:
        db.session.delete(truckDriver_object)
        db.session.commit()
        return generate_response(200, "Truck Driver", truckDriver_object.to_json(), "Truck Driver deleted with success")
    except Exception as e:
        print('Error', e)
        return generate_response(400, "Truck Driver", {}, "Error deleting truck Driver")

app.run()
