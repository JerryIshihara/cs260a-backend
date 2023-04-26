from config import ma
from model.speed import *

class SpeedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Speed