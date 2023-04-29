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

# User (user_id) book Court (court_number)
@bk_api.route('/book', methods = ['POST'])
def book_court():
    id = request.form.get('id')
    user_id = request.form.get('user_id')
    Booking.book_court(id, user_id)

    return jsonify({'message': 'Booking successful!'})

# Search courts by name, name could be null
@bk_api.route('/search', methods = ['GET'])
def search_courts():
    court_name = request.args.get('court_name')
    available_courts = Booking.get_available_courts(court_name)

    return jsonify({'courts' : available_courts})

# register routes
app.register_blueprint(bk_api)
