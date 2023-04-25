from config import db
import enum, datetime


class BillingPlan(str, enum.Enum):
    __name__ = "BillingPlan"
    FREE = "free"
    PRO = 'pro'
    PREMIUM = 'premium'


class BillingPlanEnumError(Exception):

    def __init__(self, message):
        super().__init__(message)


class Billing(db.Model):
    __tablename__ = "Billing"
    id = db.Column(db.Integer, primary_key=True)
    # AWS user id
    user_id = db.Column(db.String, unique=True, nullable=False)
    plan = db.Column(db.Enum(BillingPlan),
                     nullable=False,
                     default=BillingPlan.FREE)
    updated_on = db.Column(db.DateTime,
                           default=datetime.datetime.now(),
                           nullable=False)

    def __init__(self, user_id, plan):
        self.user_id = user_id
        self.plan = plan
        self.updated_on = datetime.datetime.now()

    def __repr__(self):
        return f"<Billing plan: {self.plan}>"

    def update(self, data: dict):
        for key in data.keys():
            setattr(self, key, data[key])
        self.updated_on = datetime.datetime.now()

    @staticmethod
    def get_plan(plan):
        try:
            bp = BillingPlan(plan)
            return bp
        except Exception as e:
            print(e)
            raise BillingPlanEnumError(
                "Invalid billing plan enum type, must be one of {free, pro, premium}"
            )
