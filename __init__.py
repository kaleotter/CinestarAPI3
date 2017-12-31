from flask import Response,json,request,jsonify, Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api, abort, fields, marshal_with, reqparse
from flask_marshmallow import Marshmallow
from json import dumps
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)


from app import view, models



