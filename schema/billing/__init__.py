from config import ma
from marshmallow_enum import EnumField
from model.billing import Billing, BillingPlan

class BillingSchema(ma.SQLAlchemyAutoSchema): 
    
    class Meta:
        model = Billing
    plan = EnumField(BillingPlan)