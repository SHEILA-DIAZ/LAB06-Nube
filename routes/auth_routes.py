from flask import Blueprint, request, jsonify
from config.database import get_db
from auth.authentication import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"mensaje": "Datos no proporcionados"}), 400

    correo = data.get('correo')
    password = data.get('password')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
    user_row = cursor.fetchone()
    conn.close()

    if not user_row:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    usuario = dict(user_row)

    if usuario['password'] != password:
        return jsonify({"mensaje": "Contraseña incorrecta"}), 401

    token = generate_token(usuario)

    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "token": token,
        "usuario": {
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "correo": usuario["correo"],
            "rol": usuario["rol"],
            "departamento": usuario["departamento"],
            "nivel_seguridad": usuario["nivel_seguridad"],
            "pais": usuario["pais"],
            "estado": usuario["estado"]
        }
    }), 200