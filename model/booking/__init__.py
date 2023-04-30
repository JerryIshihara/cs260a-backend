from enum import unique
from config import db
import datetime
import pytz

class Booking(db.Model):
    __tablename__ = "Booking"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=True)
    field_name = db.Column(db.String, nullable=False)
    court_number = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    is_booked = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)

    # User (user_id) book Court (court_number)
    def book_court(id, user_id):
        court = Booking.query.get(id)
        court.is_booked = 1
        court.user_id = user_id
        db.session.commit()

    # Court (court_number) revervation cancelled
    @staticmethod
    def cancel_booking(id):
        booking = Booking.query.get(id)
        db.session.delete(booking)
        db.session.commit()

    # Find courts that are available
    @staticmethod
    def get_available_courts(field_name):
        if field_name is None or field_name.lower() == "all":
            available_courts = Booking.query.filter_by(is_booked=0)
        else:
            available_courts = Booking.query.filter_by(is_booked=0, field_name=field_name)
        
        return [court.serialize() for court in available_courts]
    
    # Search all courts reserved by a User (user_id)
    @staticmethod
    def get_reserved_courts(user_id):
        reserved_courts = Booking.query.filter_by(is_booked=1, user_id=user_id)

        return [court.serialize() for court in reserved_courts]

    #Define a function to serialize Booking
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'field_name': self.field_name,
            'court_number': self.court_number,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'address': self.address,
            'is_booked': self.is_booked,
            'price': self.price,
            'description': self.description
        }
