from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask('flask')
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)
