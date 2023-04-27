from config import ma
from marshmallow_enum import EnumField
from model.booking import *

class BookingSchema(ma.SQLAlchemyAutoSchema): 
    
    class Meta:
        model = Booking