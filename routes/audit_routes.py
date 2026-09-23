from flask import Blueprint, jsonify
from config.database import get_db

audit_bp = Blueprint('audit', __name__)

def registrar_auditoria(usuario_nombre, recurso, accion, resultado, motivo):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO auditoria (usuario, recurso, accion, resultado, motivo)
        VALUES (?, ?, ?, ?, ?)
    ''', (usuario_nombre, recurso, accion, resultado, motivo))
    conn.commit()
    conn.close()

@audit_bp.route('/auditoria', methods=['GET'])
def obtener_auditoria():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auditoria ORDER BY id DESC")
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(logs), 200