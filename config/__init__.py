import os, datetime
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

# base directory
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# load .env file
dotenv_path = os.path.join(basedir, ".env")
load_dotenv(dotenv_path)

# init app instance
app = Flask("cs260a")

import subprocess
if not os.path.exists(os.path.join(basedir, "database/database.db")):
    command = "mkdir database && touch database/database.db"
    result = subprocess.run(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            shell=True)

# Print the output of the command
print("Output:", result.stdout)

# Print any errors that occurred
if result.stderr:
    print("Error:", result.stderr)

# settup sql-alchemy config
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir,
                                                      "database/database.db")
print(dotenv_path)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# init CORS
cors = CORS(app,
            resources={r'/*': {
                "origins": "*",
            }},
            allow_headers=[
                "Content-Type",
                "Authorization",
                "Access-Control-Allow-Credentials",
            ],
            supports_credentials=True)

# init database and schema
db = SQLAlchemy(app)
ma = Marshmallow(app)
# register all blueprints by importing api folder
from api import *
from model import *

# erase all data if needed
# db.drop_all()
with app.app_context():
    db.create_all()

# migrate changes
migrate = Migrate(app, db)
