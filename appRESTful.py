# appRESTful.py
from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# URL de la API MockAPI
api_url = "https://66ecd6b22b6cf2b89c5f711e.mockapi.io/IoTCarStatus"

# Lista para almacenar los registros temporalmente
registros = []

# Ruta para recibir datos desde appDesktop y enviarlos a MockAPI
@app.route('/procesar', methods=['POST'])
def procesar_datos():
    data = request.json
    name = data.get('name')
    status = data.get('status')
    ip_client = data.get('ipClient')
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Preparar datos para MockAPI
    datos = {
        "status": status,
        "date": date,
        "ipClient": ip_client,
        "name": name
    }

    # Enviar datos a MockAPI
    response = requests.post(api_url, data=json.dumps(datos), headers={"Content-Type": "application/json"})
    if response.status_code == 201:
        # Guardar en la lista local
        registros.append(datos)
        if len(registros) > 10:
            registros.pop(0)  # Mantener solo los últimos 10 registros
        return jsonify({"message": "Datos procesados y enviados a MockAPI", "status": "success"}), 201
    else:
        return jsonify({"message": "Error al enviar datos a MockAPI", "status": "error"}), 500

# Ruta para obtener los últimos 10 registros
@app.route('/cars', methods=['GET'])
def obtener_registros():
    return jsonify(registros), 200

if __name__ == '__main__':
    app.run(debug=True)
