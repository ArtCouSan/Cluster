from api.db.config import db

class WaterMeasurements(db.Model):
    __tablename__ = 'WaterMeasurements'
    measurement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parameter_id = db.Column(db.Integer,db.ForeignKey('WaterQualityParameters.parameter_id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    measurement_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    parameter = db.relationship('WaterQualityParameters')

class WaterQualityParameters(db.Model):
    __tablename__ = 'WaterQualityParameters'
    parameter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parameter_name = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
