# Modules
from flask import Flask, jsonify, request
import threading
import time
import os
import logging

# Creates a web-application instance
app = Flask(__name__)

# To print to the console
logging.basicConfig(level=logging.INFO)

# Sets the rate-limit (per minute)
rate_limit = 3

# This HashTable stores the time-stamps, when a user gains access (to the resource)
requests = {}

# This is a MutEx to ensure thread-safety, while modifying the above Hashtable "requests"
requests_lock = threading.Lock()

# This function removes timestamps, which are older than 60 seconds (for a specific user)
def clear_expired_requests(user_timestamps):
    for timestamp in reversed(user_timestamps):
        if time.time() - timestamp >= 60:
            user_timestamps.pop()

# This function implements rate-limiting with the Sliding Window algorithm
def allow_request():

    # Extracts user_ID and IP_address from request-headers
    user_id = request.headers.get('user-id')
    ip_address = request.headers.get('ip-address')

    # Error Check
    if not user_id or not ip_address:
        return jsonify(message='User ID or IP address not provided'), 400

    # This is the user's session-key
    key = f"{user_id}_{ip_address}"

    # Critical Section: Acquires a MutEx-lock on the hashtable "requests"
    with requests_lock:

        # Retrieves the (list of) previous time-stamps (for this user)
        user_timestamps = requests.get(key, [])

        # Removes timestamps older than 60 seconds (for this user)
        clear_expired_requests(user_timestamps)

        # If rate-limit (per minute) has been exceeded
        if len(user_timestamps) >= rate_limit:
            logging.error(f"Rate limit reached by {user_id} @ {ip_address}")
            return jsonify(message= f"Access Denied  to {user_id} @ {ip_address} :: Rate limit reached"), 429

        # Else record the current time-stamp
        user_timestamps.append(time.time())
        requests[key] = user_timestamps

    return None

@app.route('/api/resource')
def get_resource():
    return jsonify(message= f"Access Granted to {request.headers.get('user-id')} @ {request.headers.get('ip-address')}")

@app.before_request
def before_request():
    error_response = allow_request()
    if error_response:
        return error_response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
