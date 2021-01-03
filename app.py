from flask import Flask
import json
from flask import request
from datetime import datetime

from main import Cars, Bookings, Users, Bills, Locations, db

app = Flask(__name__)


@app.route('/getCar/<id>')
def getCar(id):
    carObj = Cars.query.get(int(id))
    return json.dumps(carObj.makeDict())


@app.route('/getUser/<id>')
def getUser(id):
    userObj = Users.query.get(id)
    return json.dumps(userObj.makeDict())


@app.route('/getAllUsers')
def getAllUsers():
    userObjList = Users.query.all()
    userList = list(map(lambda user: user.makeDict(),userObjList))
    return json.dumps(userList)

@app.route('/getAllCars')
def cars():
    carObjList = Cars.query.all()
    carList = list(map(lambda car: car.makeDict(), carObjList))
    return json.dumps(carList)


@app.route('/getAllBookings')
def bookings():
    bookingObjList = Bookings.query.all()
    bookingList = list(map(lambda booking: booking.makeDict(), bookingObjList))
    return json.dumps(bookingList)


@app.route('/addNewUser', methods=['GET', 'POST'])
def addUser():
    userObj = request.get_json()
    newUser = Users(email=userObj["email"], id=userObj["id"])
    db.session.add(newUser)
    db.session.commit()
    return "User added"


@app.route('/addNewBooking', methods=["GET", "POST"])
def addBooking():
    bookingObj = request.get_json()
    newBill = Bills(amount=float(bookingObj["billingPrice"]))
    db.session.add(newBill)
    newLocation = Locations(address=bookingObj["pickupLocation"])
    db.session.add(newLocation)
    db.session.commit()

    newBooking = Bookings(
        userId=bookingObj["userId"], carId=int(bookingObj["carId"]), billId=newBill.id, locationId=newLocation.id,
        fromTime=datetime.fromtimestamp(int(bookingObj["fromTime"])),
        toTime=datetime.fromtimestamp(int(bookingObj["toTime"])),
    )
    db.session.add(newBooking)
    db.session.commit()
    return "Booking Added"


@app.route('/addNewCar', methods=["GET", "POST"])
def addCar():
    carObj = request.get_json()
    db.session.add(
        Cars(
            name=carObj["name"],
            brand=carObj["brand"],
            description=carObj["description"],
            image=carObj["imageName"]
        )
    )
    db.session.commit()
    return "Car added"


if __name__ == "__main__":
    app.run(debug=True)
