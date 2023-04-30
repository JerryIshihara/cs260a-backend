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

# register routes
app.register_blueprint(bk_api)
