from enum import unique
from config import db
import datetime

fields = ['EBA', 'NCBC']
court_nums = [6, 4]
times = [(8, 14), (9, 15)]

# get all possible slots
def get_all_available_slots():
    return {fields[k]: {chr(ord('A') + i): [[j, j + 1] for j in range(times[k][0], times[k][1])]
                      for i in range(court_nums[k])} for k in range(len(fields))}

all_slots = get_all_available_slots()

# get slots that are booked
def get_occupied_slot(bookings):
    occupied = {}
    for booking in bookings:
        field_name = booking.field_name
        court_number = booking.court_number
        start_time = booking.start_time
        if field_name not in occupied:
            occupied[field_name] = {}
        if court_number not in occupied[field_name]:
            occupied[field_name][court_number] = {}
        occupied[field_name][court_number].add(start_time)
    return occupied

# get slots that are available
def filter_slots(all_slots, occupied):
    for field in all_slots:
        if field not in occupied: continue
        for court in all_slots[field]:
            if court not in occupied[field]: continue
            temp = []
            for slot in all_slots[field][court]:
                if slot[0] not in occupied[field][court]:
                    temp.append(slot)
            all_slots[field][court] = temp
    return all_slots

class Booking(db.Model):
    __tablename__ = "Booking"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    field_name = db.Column(db.String, nullable=False)
    court_number = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)

    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    @staticmethod
    def book_court(user_id, field_name, court_number, date, start_time):
        new_booking = Booking(user_id = user_id, field_name = field_name, court_number = court_number, date = date, start_time = start_time)
        db.session.add(new_booking)
        db.session.commit()

    @staticmethod
    def delete_booking(id):
        old_booking = db.query.get(id)
        db.session.delete(old_booking)
        db.session.commit()

    @staticmethod
    def check_available_time(date):
        bookings: list[Booking] = Booking.query.filter_by(date=date)
        # occupied = {'EBA': {'A': {9, 10}, 'C': {10, 12}}, 'NCBC': {'B': {13}}}
        occupied = get_occupied_slot(bookings)
        filtered_slots = filter_slots(all_slots, occupied)
        return filtered_slots
