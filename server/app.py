from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    # Retrieve all messages from database and order by creation time
    messages_list = Message.query.order_by(Message.created_at.asc()).all()
    # Serialize the messages to JSON format
    return jsonify([message.to_dict() for message in messages_list])

@app.route('/messages', methods=['POST'])
def create_message():
    # Extract JSON data from the request body
    data = request.get_json()
    # Create a new message with the provided body and username
    new_message = Message(body=data['body'], username=data['username'])
    # Add the message to the database session
    db.session.add(new_message)
    # Commit changes to persist the message in the database
    db.session.commit()
    # Return the newly created message as JSON
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    # Query the database to find the message with the given id
    message = Message.query.get(id)
    if not message:
        # Return error if message not found
        return jsonify({'error': 'Message not found'}), 404
    # Extract JSON data from request
    data = request.get_json()
    # Update the message body with the new value
    message.body = data['body']
    # Commit changes to persist updates
    db.session.commit()
    # Return the updated message as JSON
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    # Query the database to find the message with the given id
    message = Message.query.get(id)
    if not message:
        # Return error if message not found
        return jsonify({'error': 'Message not found'}), 404
    # Delete the message from the database session
    db.session.delete(message)
    # Commit changes to persist deletion
    db.session.commit()
    # Return empty response with 204 No Content status
    return '', 204

if __name__ == '__main__':
    app.run(port=5555)
