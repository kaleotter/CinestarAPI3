
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #define config stuff here
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:student@localhost/cinestar'
    SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:student@cr.cinestar-internal.lan/cinestar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = True  