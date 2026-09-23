from authorization.rbac import evaluar_rbac
from authorization.abac import evaluar_abac

def evaluar_acceso(usuario, documento, operacion, entorno):
    # Etapa 1: RBAC
    rbac_ok, rbac_msg = evaluar_rbac(usuario.get("rol"), operacion)
    if not rbac_ok:
        return False, f"DENEGADO POR RBAC: {rbac_msg}", "RBAC"

    # Etapa 2: ABAC
    abac_ok, abac_msg = evaluar_abac(usuario, documento, operacion, entorno)
    if not abac_ok:
        return False, f"DENEGADO POR ABAC: {abac_msg}", "ABAC"

    return True, "AUTORIZADO: RBAC y ABAC cumplidos con éxito", "OK"