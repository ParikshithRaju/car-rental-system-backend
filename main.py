from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import base64

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql12383945:krqQaJ1XHb@sql12.freemysqlhosting.net/sql12383945'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://me:Wasupmynigga1#@localhost/car_rental_system'
db = SQLAlchemy(app)


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(120),
                      unique=True)  # Give the name of the image which will be present in the server's
    # /assets/carImages
    bookings = db.relationship('Bookings', backref='car', lazy=True)

    def makeDict(self):
        image_bs4_string = ""
        with open("assets/carImages/" + self.image, "rb") as image_file:
            image_bs4_string = base64.b64encode(image_file.read())
        return {
            "name": self.name,
            "id": self.id,
            "brand": self.brand,
            "description": self.description,
            "image": image_bs4_string.decode("utf-8"),
            "bookings": list(map(lambda booking: booking.makeDict(), self.bookings))
        }


class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)
    carId = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    billId = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=False)
    locationId = db.Column(db.Integer, db.ForeignKey('locations.id'))
    fromTime = db.Column(db.DateTime)
    toTime = db.Column(db.DateTime)

    def makeDict(self):
        if self.pickupLocation:
            return {
                "id": self.id,
                "userId": self.userId,
                "carId": self.carId,
                "fromTime": str(self.fromTime),
                "toTime": str(self.toTime),
                "pickupLocation": self.pickupLocation.address,
                "billingPrice": self.bill.amount
            }
        else:
            return {
                "id": self.id,
                "userId": self.userId,
                "carId": self.carId,
                "fromTime": str(self.fromTime),
                "toTime": str(self.toTime),
                "pickupLocation": "none",
                "billingPrice": self.bill.amount
            }



class Users(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    bookings = db.relationship('Bookings', backref="user", lazy=True)

    def makeDict(self):
        return {
            "id": self.id,
            "email": self.email,
            "bookings": list(map(lambda booking: booking.makeDict(), self.bookings))
        }


class Bills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now)
    amount = db.Column(db.Float, nullable=False)
    booking = db.relationship('Bookings', backref="bill", lazy=True)


class Locations(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    address = db.Column(db.Text,nullable=False)
    booking = db.relationship('Bookings',backref="pickupLocation",lazy=True)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    db.session.add(Users(id="z7tXH8JGghPDNuzU2c7dBCJsud23", email="rpari490@gmail.com"))
    db.session.add(Cars(name="Fortuner", brand="Toyota",image="fortuner.png",description="Toyota Fortuner is the "
                                                                                         "best in class luxury suv in"
                                                                                         " India. This sports utility "
                                                                                         "vehicle comes in both 4wd and"
                                                                                         " 2wd varients. "))
    db.session.add(Cars(name="i20", brand="Hyundai",image="i20.png",description="The all-new i20 is all set to take to "
                                                                               "create new benchmarks in the industry"
                                                                               " and market with its charismatic "
                                                                               "stance. "))
    db.session.add(Bills(amount=120.2))
    db.session.add(Bookings(carId=2, userId="z7tXH8JGghPDNuzU2c7dBCJsud23", billId=1, fromTime=datetime.now(),
                            toTime=datetime.now(),
                            ))
    db.session.add(Cars(name="GTR", brand="Nissan",
                        description="At the heart of the GT-R is an ideally sized, twin-turbocharged 3.8-L V6 that "
                                    "produces a prodigious 570 ps and equally immense 637 nm of torque.",
                        image="nissan-gtr.png"))
    db.session.add(Cars(name="Chiron", brand="Bugati",
                        description="The Chiron is Bugatti\'s natural successor to the Veyron. Powered by a 8.0-litre "
                                    "quad-turbocharged W16 engine that makes a whopping 1500PS of power and 1600Nm of "
                                    "torque, the Chiron can do the 0-100kmph run in just 2.5 seconds. ... Bugatti "
                                    "will build the Chiron only in limited numbers, 500 to be exact.",
                        image="bugati-chiron.png"))
    db.session.add(Cars(name="Veyron", brand="Bugati",
                        description="The Bugatti Veyron EB 16.4 is a mid-engine sports car, designed and developed in "
                                    "Germany by the Bugatti Engineering GmbH and manufactured by the Bugatti "
                                    "Automobiles SAS in Molsheim, France.",
                        image="bugati-veyron.png"))
    db.session.add(Cars(name="Aventador", brand="Lamborghini",
                        description="The Aventador S expresses unmistakable Lamborghini DNA, adding even more "
                                    "dynamism, refinement and aggressiveness through its finely honed features.",
                        image="lamborginiAventedor.png"))

    db.session.commit()
