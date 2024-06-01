from flask import Blueprint, request, jsonify, current_app
from concurrent.futures import ThreadPoolExecutor
from dask import delayed, compute
import pandas as pd
from api.db.models import WaterMeasurements
from api.db.config import db

sensor_blueprint = Blueprint('sensor', __name__)
executor = ThreadPoolExecutor(max_workers=4)


@sensor_blueprint.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data:
        app = current_app._get_current_object()
        executor.submit(process_data, data, app)
        return jsonify(data), 202
    else:
        return jsonify({"error": "No data provided"}), 400


def process_data(data, app):
    with app.app_context():
        try:
            parameters = {
                'temperature': 1,
                'dissolved_oxygen': 2,
                'salinity': 3,
                'turbidity': 4,
                'microplastics': 5
            }
            for key, value in data.items():
                parameter_id = parameters.get(key)
                if parameter_id:
                    measurement = WaterMeasurements(parameter_id=parameter_id, value=value['value'])
                    db.session.add(measurement)
            db.session.commit()
            print("Data processed and committed to the database", flush=True)
        except Exception as e:
            error_message = f"Error processing data: {str(e)}"
            print(error_message, flush=True)
            db.session.rollback()
            print("Transaction rolled back due to an error.", flush=True)


@sensor_blueprint.route('/sensor-data', methods=['GET'])
def get_data():
    measurements = fetch_data()
    return jsonify(measurements), 200


def fetch_data():
    measurements = WaterMeasurements.query.all()
    return [{'parameter_id': m.parameter_id, 'value': m.value} for m in measurements]
