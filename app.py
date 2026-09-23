from flask import Flask, jsonify
from flask_cors import CORS
from config.database import init_db

app = Flask(__name__)
CORS(app)

# Inicializar Base de Datos
init_db()

@app.route('/')
def home():
    return jsonify({
        "sistema": "SecureDocs",
        "estado": "Servicio de Autenticación y Base de Datos Configurados",
        "mensaje": "Aplicación lista para implementar RBAC + ABAC"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)