from flask import Blueprint, request, jsonify, current_app, g
from dask import delayed, compute
from sqlalchemy.orm import scoped_session, sessionmaker
from api.db.models import WaterMeasurements
from api.db.config import db

sensor_blueprint = Blueprint('sensor', __name__)


def get_session():
    if 'db_session' not in g:
        g.db_session = scoped_session(sessionmaker(bind=db.engine))
    return g.db_session


@sensor_blueprint.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data:
        app = current_app._get_current_object()
        process_data(data, app)
        return jsonify(data), 202
    else:
        return jsonify({"error": "No data provided"}), 400


def process_data(data, app):
    parameters = {
        'temperature': 1,
        'dissolved_oxygen': 2,
        'salinity': 3,
        'turbidity': 4,
        'microplastics': 5
    }
    tasks = []
    for key, value in data.items():
        parameter_id = parameters.get(key, None)
        if parameter_id:
            task = delayed(insert_measurement)(parameter_id, value['value'], app)
            tasks.append(task)
    compute(*tasks)


def insert_measurement(parameter_id, value, app):
    with app.app_context():
        session = get_session()
        try:
            measurement = WaterMeasurements(parameter_id=parameter_id, value=value)
            session.add(measurement)
            session.commit()
        finally:
            session.remove()


@sensor_blueprint.route('/sensor-data', methods=['GET'])
def get_data():
    measurements = fetch_data()
    return jsonify(measurements), 200


def fetch_data():
    session = get_session()
    measurements = session.query(WaterMeasurements).all()
    return [{'parameter_id': m.parameter_id, 'value': m.value} for m in measurements]


@sensor_blueprint.teardown_app_request
def remove_session(exception=None):
    if 'db_session' in g:
        g.db_session.remove()
