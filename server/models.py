from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    # Define body attribute to store the message content
    body = db.Column(db.String, nullable=False)
    # Define username attribute to track who sent the message
    username = db.Column(db.String, nullable=False)
    # Set created_at with default value to current time
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Set updated_at with default value to current time
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
