from datetime import datetime

def evaluar_abac(usuario, documento, operacion, entorno):
    # Política 7 — Estado del usuario
    if usuario.get("estado") != "ACTIVO":
        return False, "Usuario inactivo o suspendido"

    # Política 8 — Invitados
    if usuario.get("rol") == "INVITADO":
        if (usuario.get("tipo_contrato") == "EXTERNO" and 
            documento.get("nivel_confidencialidad", 5) <= 1 and 
            documento.get("estado") == "PUBLICADO"):
            return True, "Acceso concedido a invitado"
        return False, "Invitado no cumple las condiciones de acceso"

    # Política 1 — Departamento (para operaciones de consulta/modificación)
    if usuario.get("rol") not in ["ADMINISTRADOR", "GERENTE"]:
        if usuario.get("departamento") != documento.get("departamento"):
            return False, "El usuario no pertenece al departamento del documento"

    # Política 2 — Nivel de seguridad
    if usuario.get("nivel_seguridad", 0) < documento.get("nivel_confidencialidad", 5):
        return False, "Nivel de seguridad del usuario insuficiente para la confidencialidad del documento"

    # Política 3 — Propiedad (al modificar)
    if operacion == "MODIFICAR":
        if usuario.get("rol") not in ["ADMINISTRADOR", "GERENTE"]:
            if usuario.get("id") != documento.get("propietario"):
                return False, "Un empleado solo puede modificar sus propios documentos"

    # Política 4 — Horario (Documentos confidenciales >= 4 solo de 08:00 a 18:00)
    if documento.get("nivel_confidencialidad", 0) >= 4:
        hora_actual = entorno.get("hora_obj", datetime.now().time())
        inicio = datetime.strptime("08:00", "%H:%M").time()
        fin = datetime.strptime("18:00", "%H:%M").time()
        if not (inicio <= hora_actual <= fin):
            return False, "Acceso denegado fuera del horario permitido (08:00 - 18:00) para nivel confidencial"

    # Política 5 — País
    if usuario.get("pais") != documento.get("pais"):
        return False, "El país del usuario no coincide con el del documento"

    # Política 6 — Dispositivo (Nivel >= 4 solo desde dispositivo CORPORATIVO)
    if documento.get("nivel_confidencialidad", 0) >= 4:
        if entorno.get("dispositivo") != "CORPORATIVO":
            return False, "Documentos altamente confidenciales requieren dispositivo CORPORATIVO"

    return True, "ABAC PERMITIDO"