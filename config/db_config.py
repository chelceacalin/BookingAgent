from .flask_config import app
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.db.Tables import *