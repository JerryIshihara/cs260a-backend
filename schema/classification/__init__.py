# User Schema
from config import ma
from model.classification import *

class ClassificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Classification
        
        
# class GroupMemberSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = KaggleGroupMember
