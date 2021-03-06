from flask import Flask
import psycopg2

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON


app = Flask(__name__)

# ADD
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://webopenfx:tuttle@localhost:5432/webopenfx_db"

db = SQLAlchemy(app)

class Plugin(db.Model):

    '''
    This is the representation as an object and as seen from the DB perspective
    '''

    __tablename__ = 'plugin'
    '''
    Representation of a Plugin in the DB
    '''
    id = db.Column(db.Integer, primary_key=True)
    # The pluginID isn't generated in the Class but some other instance, hence the primary key type
    pluginId = db.Column(UUID, unique=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    shortDescription = db.Column(db.String(250), nullable=False)
    version = db.Column(db.String(250), nullable=False)
    # These colomn might become Custom Types, until then, we stock it as JSON
    clip = db.Column(JSON)
    parameters = db.Column(JSON, nullable=False)
    properties = db.Column(JSON, nullable=False)
    tags = db.Column(JSON)
    presets = db.Column(JSON)
    rate = db.Column(db.Integer)
    defautImagePath = db.Column(ARRAY(db.String), nullable=False)
    # Can be empty this it is for user's personnal image sample
    sampleImagePath = db.Column(ARRAY(db.String))


db.create_all()
