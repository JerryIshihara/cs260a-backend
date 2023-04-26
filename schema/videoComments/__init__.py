from config import ma
from model.videoComments import *

class videoCommentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VideoComments