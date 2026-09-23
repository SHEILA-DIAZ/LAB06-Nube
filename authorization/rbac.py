# Matriz de Permisos RBAC según la tabla del laboratorio
MATRIZ_RBAC = {
    "ADMINISTRADOR": ["CREAR", "CONSULTAR", "MODIFICAR", "ELIMINAR", "APROBAR", "VER_AUDITORIA", "GESTIONAR_USUARIOS", "ASIGNAR_ROLES"],
    "GERENTE":       ["CREAR", "CONSULTAR", "MODIFICAR", "ELIMINAR", "APROBAR", "VER_AUDITORIA"],
    "SUPERVISOR":    ["CREAR", "CONSULTAR", "MODIFICAR", "APROBAR"],
    "EMPLEADO":      ["CREAR", "CONSULTAR", "MODIFICAR"],
    "AUDITOR":       ["CONSULTAR", "VER_AUDITORIA"],
    "INVITADO":      ["CONSULTAR"]
}

def evaluar_rbac(rol_usuario, operacion):
    permisos = MATRIZ_RBAC.get(rol_usuario, [])
    if operacion in permisos:
        return True, "RBAC PERMITIDO"
    return False, f"El rol {rol_usuario} no tiene permiso para la operación '{operacion}'"