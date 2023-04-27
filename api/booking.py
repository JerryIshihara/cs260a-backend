from flask import request, Blueprint, jsonify, Response, flash, url_for, send_from_directory
from marshmallow import ValidationError
from model.booking import *
from schema.booking import BookingSchema
from config import app, db

cls_api = Blueprint("cls_api", __name__, url_prefix="/api/booking")

def book_court(user_id, field_name, court_number, date, start_time, end_time):
    Booking.book_court(user_id, field_name, court_number, date, start_time, end_time)

def check_available_time(date):
    return Booking.check_available_time(date)

def delete_booking(user_id, field_name, court_number, date, start_time, end_time):
    Booking.delete_booking(user_id, field_name, court_number, date, start_time, end_time)

@cls_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
def cls_crud():
    try:
        result = {}
    
        if request.method == "GET":
            # check_available_time
            date = request.args.get("date")
            result = {'avalibility': check_available_time(date)}
        
        elif request.method == "POST":
            # book_court
            user_id = request.args.get("user_id")
            field_name = request.args.get("field_name")
            court_number = request.args.get("court_number")
            date = request.args.get("date")
            start_time = request.args.get("start_time")
            end_time = request.args.get("end_time")
            book_court(user_id, field_name, court_number, date, start_time, end_time)

        elif request.method == "DELETE":
            # delete_booking
            user_id = request.args.get("user_id")
            field_name = request.args.get("field_name")
            court_number = request.args.get("court_number")
            date = request.args.get("date")
            start_time = request.args.get("start_time")
            end_time = request.args.get("end_time")
            delete_booking(user_id, field_name, court_number, date, start_time, end_time)

        return jsonify(result), 200

    except Exception as e:
        print(e)
        return "Server Error", 500


# register routes
app.register_blueprint(cls_api)
