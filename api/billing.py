from flask import request, Blueprint, jsonify, Response, flash, url_for, send_from_directory
from marshmallow import ValidationError
from model.billing import *
from schema.billing import BillingSchema
from config import app, db

billing_api = Blueprint("billing_api", __name__, url_prefix="/api/billing")


@billing_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
def billing_crud():
    try:
        user_id = request.args.get('u')
        plan = request.args.get('plan')  # BillingPlan

        # check if user exists
        billing = Billing.query.filter_by(user_id=user_id).first()

        if request.method == "GET":
            billing_scheme = BillingSchema(exclude=["id"])
            result = billing_scheme.dump(billing)

        if request.method == "POST":
            if billing:
                return jsonify(
                    {"message": "Billing subscription already exists"}), 400
            billing = Billing(user_id, Billing.get_plan(plan))
            db.session.add(billing)
            db.session.commit()
            result = {"message": "Billing subscription created successfully"}

        if request.method == "PUT":
            if not billing:
                return jsonify(
                    {"message": "Billing subscription does not exist"}), 400
            billing = Billing.query.filter_by(user_id=user_id).first()
            billing.update({"plan": Billing.get_plan(plan)})
            db.session.commit()
            result = {"message": "Billing subscription updated successfully"}

        if request.method == "DELETE":
            if not billing:
                return jsonify(
                    {"message": "Billing subscription does not exist"}), 400
            billings = Billing.query.filter_by(user_id=user_id).all()
            db.session.delete(billings)
            db.session.commit()
            result = {"message": "Billing subscription cancelled successfully"}
        return jsonify(result), 200

    except ValidationError as e:
        return jsonify({"Invalid request": str(e)}), 400
    except BillingPlanEnumError as e:
        return jsonify({"Invalid request": str(e)}), 400
    except Exception as e:
        print(e)
        return "Server Error", 500


# register routes
app.register_blueprint(billing_api)
