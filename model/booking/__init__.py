from enum import unique
from config import db
import datetime

fields = ['EBA', 'NCBC']
court_nums = [6, 4]
times = [(8, 14), (9, 15)]

def get_all_available_slots():
    return {fields[k]: {chr(ord('A') + i): [[j, j + 1] for j in range(times[k][0], times[k][1])]
                      for i in range(court_nums[k])} for k in range(len(fields))}

all_slots = get_all_available_slots()

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
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    field_name = db.Column(db.String, nullable=False)
    court_number = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)

    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    def book_court(self, user_id: str, field_name: str, court_number: str, date: str, start_time: int, end_time: int):
        for i in range(start_time, end_time):
            id = user_id + field_name + court_number + date + i
            new_booking = Booking(id, user_id = user_id, field_name = field_name, court_number = court_number, date = date, start_time = i, end_time = i + 1)
            db.session.add(new_booking)
            db.session.commit()
    
    def delete_booking(self, user_id: str, field_name: str, court_number: str, date: str, start_time: int, end_time: int):
        for i in range(start_time, end_time):
            id = user_id + field_name + court_number + date + start_time
            old_booking = Booking(id, user_id = user_id, field_name = field_name, court_number = court_number, date = date, start_time = i, end_time = i + 1)
            db.session.delete(old_booking)
            db.session.commit()

    def check_available_time(self, date: str):
        bookings: list[Booking] = Booking.query.filter_by(date=date)
        # occupied = {'EBA': {'A': {9, 10}, 'C': {10, 12}}, 'NCBC': {'B': {13}}}
        occupied = get_occupied_slot(bookings)
        filtered_slots = filter_slots(all_slots, occupied)
        return filter_slots


    # # insert a record of video with pose inference
    # def insert_video(self, id, user_id = '', video_key = ''):
    #     new_video = Speed(id = id, user_id = user_id, video_key = video_key, csv_path = str(id))
    #     db.session.add(new_video)
    #     db.session.commit()

    # def query_video(self, id):
    #     return Speed.query.get(id)