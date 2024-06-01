USE sensordb;

SET time_zone = '-03:00';

CREATE TABLE WaterQualityParameters (
    parameter_id INT AUTO_INCREMENT PRIMARY KEY,
    parameter_name VARCHAR(50) NOT NULL,
    unit VARCHAR(20) NOT NULL
);

CREATE TABLE WaterMeasurements (
    measurement_id INT AUTO_INCREMENT PRIMARY KEY,
    parameter_id INT NOT NULL,
    value DECIMAL(10, 2) NOT NULL,
    measurement_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parameter_id) REFERENCES WaterQualityParameters(parameter_id)
);
