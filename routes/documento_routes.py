from flask import Blueprint, request, jsonify
from datetime import datetime
from config.database import get_db
from authorization.engine import evaluar_acceso
from routes.audit_routes import registrar_auditoria

doc_bp = Blueprint('documento', __name__)

@doc_bp.route('/documentos/evaluar', methods=['POST'])
def evaluar_operacion_documento():
    data = request.get_json() or {}
    
    usuario = data.get('usuario')
    documento = data.get('documento')
    operacion = data.get('operacion')
    entorno = data.get('entorno', {})

    if not usuario or not documento or not operacion:
        return jsonify({"mensaje": "Datos incompletos"}), 400

    # Procesar hora si viene como string HH:MM
    if 'hora' in entorno and isinstance(entorno['hora'], str):
        entorno['hora_obj'] = datetime.strptime(entorno['hora'], "%H:%M").time()
    else:
        entorno['hora_obj'] = datetime.now().time()

    autorizado, mensaje, etapa = evaluar_acceso(usuario, documento, operacion, entorno)

    resultado_str = "PERMITIDO" if autorizado else "DENEGADO"
    recurso_str = f"documento-{documento.get('id', 'N/A')}"

    # Registrar en Auditoría (Requisito 14 del Lab)
    registrar_auditoria(
        usuario_nombre=usuario.get('correo', 'desconocido'),
        recurso=recurso_str,
        accion=operacion,
        resultado=resultado_str,
        motivo=mensaje
    )

    return jsonify({
        "autorizado": autorizado,
        "resultado": resultado_str,
        "etapa_fallo": etapa if not autorizado else None,
        "mensaje": mensaje,
        "evaluacion": {
            "usuario": usuario['nombre'],
            "rol": usuario['rol'],
            "operacion": operacion,
            "documento": documento['titulo']
        }
    }), 200 if autorizado else 403