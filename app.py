from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to avoid duplicate logic
def find_event_by_id(event_id):
    return next((e for e in events if e.id == event_id), None)

# 1. Welcome route - Required by rubric
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Events API"}), 200

# 2. GET /events - Required by rubric
@app.route('/events', methods=['GET'])
def get_events():
    return jsonify([e.to_dict() for e in events]), 200

# 3. TODO: POST /events - Create a new event from JSON input
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()

    # Input Validation - 400 if missing
    if not data or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400

    # Generate new ID - max id + 1
    new_id = max([e.id for e in events], default=0) + 1
    new_event = Event(id=new_id, title=data['title'])
    
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

# 4. TODO: PATCH /events/<id> - Update the title of an event
@app.route('/events/<int:id>', methods=['PATCH'])
def update_event(id):
    data = request.get_json()
    event = find_event_by_id(id)

    # Resource Not Found - 404
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Update title if provided
    if data and 'title' in data:
        event.title = data['title']

    return jsonify(event.to_dict()), 200

# 5. TODO: DELETE /events/<id> - Remove an event from the list
@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    global events
    event = find_event_by_id(id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    events = [e for e in events if e.id != id]
    return jsonify({"message": "Event deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
