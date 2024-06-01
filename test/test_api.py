import requests

# URL do servidor Flask
base_url = 'http://localhost:30007'

def test_post_sensor_data():
    # Dados de exemplo para enviar ao endpoint POST
    sensor_data = {
        'temperature': {'value': 22.5},
        'dissolved_oxygen': {'value': 9.3},
        'salinity': {'value': 35.0},
        'turbidity': {'value': 15.2},
        'microplastics': {'value': 0.02}
    }
    
    # Enviar requisição POST
    response = requests.post(f"{base_url}/sensor-data", json=sensor_data)
    print("Status Code for POST:", response.status_code)
    print("Response Data for POST:", response.json())

def test_get_sensor_data():
    # Enviar requisição GET
    response = requests.get(f"{base_url}/sensor-data")
    print("Status Code for GET:", response.status_code)
    print("Response Data for GET:", response.json())

if __name__ == "__main__":
    test_post_sensor_data()
    test_get_sensor_data()
