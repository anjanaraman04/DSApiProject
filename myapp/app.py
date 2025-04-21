from flask import Flask, jsonify, request
import pandas as pd 
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
import os
from functools import wraps


app = Flask(__name__)
API_TOKEN = "supersecrettoken123"
CSV_PATH = os.path.join(app.root_path, "static", "capitals.csv")
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

def load_timezones(path):
    df = pd.read_csv(path, usecols=['city','timezone'])
    df['city'] = df['city'].str.strip().str.capitalize()
    df['timezone'] = df['timezone'].str.strip()
    df = df.dropna(subset=['city','timezone'])
    return df.set_index('city')['timezone'].to_dict()


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/api/secure_data', methods=['GET'])
@token_required
def secure_data():
    return jsonify({"secret": "This is protected info!"})

@app.route('/api/time/<city_name>', methods=['GET'])
@token_required
def get_city_time(city_name):
    CITY_TIMEZONES = load_timezones(CSV_PATH)
    city_key = city_name.capitalize()
    city_timezone = CITY_TIMEZONES.get(city_key)
    if not city_timezone:
         return jsonify({
            "error": "City not found",
            "message": (
                f"'{city_name}' is not in our database. "
                f"Supported capitals: {', '.join(sorted(CITY_TIMEZONES.keys()))}."
            )
        }), 404
    now = datetime.now(ZoneInfo(city_timezone))
    offset_raw = now.strftime('%z')
    utc_offset = f"{offset_raw[:3]}:{offset_raw[3:]}"

    return jsonify({
        "city": city_key,
        "datetime": now.isoformat(),
        "utc_offset": utc_offset
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000, debug=True)
