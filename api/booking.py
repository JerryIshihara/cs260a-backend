from flask import request, Blueprint, jsonify, Response, flash, url_for, send_from_directory
from marshmallow import ValidationError
from model.booking import *
from schema.booking import BookingSchema
from config import app, db

bk_api = Blueprint("bk_api", __name__, url_prefix="/api/booking")

# Test connection
@bk_api.route('/test', methods = ['GET'])
def test():
    return jsonify({'message': 'Connection established!'})

# User (user_id) book Court (id)
@bk_api.route('/reserve', methods = ['POST'])
def book_court():
    data = request.get_json()
    id = data.get('id')
    user_id = data.get('user_id')
    Booking.book_court(id, user_id)

    return jsonify({'message': 'Booking successful!'})

# Search all available courts by name, name could be null
@bk_api.route('/search', methods = ['GET'])
def search_courts():
    court_name = request.args.get('name')
    available_courts = Booking.get_available_courts(court_name)

    return jsonify({'courts' : available_courts})


# Search all courts reserved by a User (user_id)
@bk_api.route('/getReserve', methods = ['GET'])
def get_reserved_courts():
    user_id = request.args.get('user_id')
    reserved_courts = Booking.get_reserved_courts(user_id)

    return jsonify({'courts' : reserved_courts})

# User cancel Court (id)
@bk_api.route('/cancel_reserve', methods = ['POST'])
def cancel_reserve():
    data = request.get_json()
    id = data.get('id')
    Booking.cancel_reserve(id)

    return jsonify({'message': 'Booking successful!'})

# register routes
app.register_blueprint(bk_api)
