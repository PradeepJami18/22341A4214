from flask import Flask, request, jsonify, redirect
from logger import CustomLogger
from models import URLMapping
from storage import get_shortcode, save_shortcode, shortcode_exists
import string
import random
import datetime

app = Flask(__name__)
logger = CustomLogger()

HOSTNAME = 'localhost'
PORT = 5000

# Function to generate random shortcode
def generate_shortcode(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        shortcode = ''.join(random.choices(characters, k=length))
        if not shortcode_exists(shortcode):
            return shortcode

# Middleware to log every request
@app.before_request
def log_request():
    logger.log(f"Request: {request.method} {request.path}")

# Endpoint to create a short URL
@app.route('/shorturls', methods=['POST'])
def create_shorturl():
    data = request.get_json()

    if not data or 'url' not in data:
        logger.log("Missing URL in request", "ERROR")
        return jsonify({"error": "URL is required"}), 400

    original_url = data['url']
    validity = data.get('validity', 30)
    shortcode = data.get('shortcode')

    if shortcode:
        if not shortcode.isalnum() or len(shortcode) > 10:
            logger.log(f"Invalid shortcode: {shortcode}", "ERROR")
            return jsonify({"error": "Shortcode must be alphanumeric and up to 10 chars"}), 400
        if shortcode_exists(shortcode):
            logger.log(f"Shortcode collision: {shortcode}", "ERROR")
            return jsonify({"error": "Shortcode already exists"}), 409
    else:
        shortcode = generate_shortcode()

    url_mapping = URLMapping(original_url, shortcode, validity)
    save_shortcode(shortcode, url_mapping)

    expiry_time = url_mapping.get_expiry_time().isoformat() + 'Z'
    short_link = f"http://{HOSTNAME}:{PORT}/{shortcode}"

    logger.log(f"Short URL created: {shortcode} -> {original_url}")
    return jsonify({
        "shortLink": short_link,
        "expiry": expiry_time
    }), 201

# Endpoint to get statistics of a short URL
@app.route('/shorturls/<shortcode>', methods=['GET'])
def get_statistics(shortcode):
    mapping = get_shortcode(shortcode)

    if not mapping:
        logger.log(f"Statistics request for non-existent shortcode: {shortcode}", "ERROR")
        return jsonify({"error": "Shortcode does not exist"}), 404

    return jsonify({
        "original_url": mapping.original_url,
        "created_at": mapping.creation_time.isoformat() + 'Z',
        "expiry": mapping.get_expiry_time().isoformat() + 'Z',
        "clicks": len(mapping.clicks),
        "click_details": [click.to_dict() for click in mapping.clicks]
    }), 200

# Endpoint to redirect to the original URL
@app.route('/<shortcode>', methods=['GET'])
def redirect_shorturl(shortcode):
    mapping = get_shortcode(shortcode)

    if not mapping:
        logger.log(f"Access attempt for non-existent shortcode: {shortcode}", "ERROR")
        return jsonify({"error": "Shortcode not found"}), 404

    if mapping.is_expired():
        logger.log(f"Access attempt for expired shortcode: {shortcode}", "ERROR")
        return jsonify({"error": "Shortcode expired"}), 410

    referrer = request.referrer or "Direct"
    location = request.headers.get('X-App-Location', 'Unknown')

    mapping.add_click(referrer, location)
    logger.log(f"Redirecting {shortcode} to {mapping.original_url}")

    return redirect(mapping.original_url)

# Handler for 404 errors
@app.errorhandler(404)
def handle_404(e):
    logger.log(f"404 Not Found: {request.path}", "ERROR")
    return jsonify({"error": "Endpoint not found"}), 404

# Handler for 500 errors
@app.errorhandler(500)
def handle_500(e):
    logger.log(f"500 Server Error: {str(e)}", "ERROR")
    return jsonify({"error": "Internal server error"}), 500

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
