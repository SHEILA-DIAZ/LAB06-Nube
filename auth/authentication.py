import jwt
import datetime

SECRET_KEY = "clave_secreta_securedocs_lab06"

def generate_token(usuario):
    payload = {
        "id": usuario["id"],
        "nombre": usuario["nombre"],
        "correo": usuario["correo"],
        "rol": usuario["rol"],
        "departamento": usuario["departamento"],
        "nivel_seguridad": usuario["nivel_seguridad"],
        "pais": usuario["pais"],
        "tipo_contrato": usuario["tipo_contrato"],
        "estado": usuario["estado"],
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None