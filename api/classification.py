from flask import request, Blueprint, jsonify, Response, flash, url_for, send_from_directory
from marshmallow import ValidationError
from model.classification import *
from schema.classification import ClassificationSchema
from config import app, db

cls_api = Blueprint("cls_api", __name__, url_prefix="/api/classification")


@cls_api.route("/", methods=["GET", "POST", "DELETE", "PUT"])
def cls_crud():
    pass


# register routes
app.register_blueprint(cls_api)
