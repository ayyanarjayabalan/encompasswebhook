from flask import Flask, request, jsonify
from flask_caching import Cache

app = Flask(__name__)

# Configure cache (using simple cache for demonstration purposes)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.cache = Cache(app)

# Cache key for storing webhook events
CACHE_KEY = 'webhook_events'

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    """Receive webhook events and store them in cache."""
    event = request.json
    if not event:
        return jsonify({"error": "Invalid event data"}), 400

    # Get existing events from cache
    events = app.cache.get(CACHE_KEY) or []
    
    # Append new event to the list
    events.append(event)
    app.cache.set(CACHE_KEY, events)

    return jsonify({"message": "Event stored successfully"}), 200

@app.route('/webhook/events', methods=['GET'])
def get_events():
    """Retrieve all stored events from the cache."""
    events = app.cache.get(CACHE_KEY) or []
    return jsonify(events), 200

@app.route('/webhook/events', methods=['DELETE'])
def delete_events():
    """Delete all events from the cache."""
    app.cache.delete(CACHE_KEY)
    return jsonify({"message": "All events deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
