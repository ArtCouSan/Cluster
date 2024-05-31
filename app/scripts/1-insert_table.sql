USE sensordb;

INSERT INTO WaterQualityParameters (parameter_name, unit)
VALUES
('temperature', 'C'),
('dissolved_oxygen', 'mg/L'),
('salinity', 'ppt'),
('turbidity', 'NTU'),
('microplastics', 'particles/m^3');
