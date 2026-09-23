import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../database/securedocs.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()

    # Tabla Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL,
            departamento TEXT NOT NULL,
            nivel_seguridad INTEGER NOT NULL,
            pais TEXT NOT NULL,
            tipo_contrato TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    ''')

    # Tabla Documentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            propietario INTEGER NOT NULL,
            departamento TEXT NOT NULL,
            nivel_confidencialidad INTEGER NOT NULL,
            estado TEXT NOT NULL,
            pais TEXT NOT NULL,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (propietario) REFERENCES usuarios (id)
        )
    ''')

    # Tabla Auditoría
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            recurso TEXT NOT NULL,
            accion TEXT NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            resultado TEXT NOT NULL,
            motivo TEXT NOT NULL
        )
    ''')

    # Poblado inicial de usuarios de prueba (Laboratorio)
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        usuarios = [
            (25, 'Ana Torres', 'ana.torres@techcorp.com', '123456', 'SUPERVISOR', 'FINANZAS', 3, 'PERU', 'INTERNO', 'ACTIVO'),
            (10, 'Carlos Ruiz', 'carlos.ruiz@techcorp.com', '123456', 'SUPERVISOR', 'FINANZAS', 3, 'PERU', 'INTERNO', 'ACTIVO'),
            (11, 'Lucia Mendez', 'lucia.mendez@techcorp.com', '123456', 'EMPLEADO', 'RRHH', 2, 'PERU', 'INTERNO', 'ACTIVO'),
            (12, 'Juan Perez', 'juan.perez@techcorp.com', '123456', 'GERENTE', 'FINANZAS', 4, 'PERU', 'INTERNO', 'ACTIVO'),
            (13, 'Pedro Admin', 'admin@techcorp.com', '123456', 'ADMINISTRADOR', 'TI', 5, 'PERU', 'INTERNO', 'ACTIVO'),
            (14, 'Maria Auditora', 'auditora@techcorp.com', '123456', 'AUDITOR', 'AUDITORIA', 5, 'PERU', 'INTERNO', 'ACTIVO'),
            (15, 'Invitado Externo', 'invitado@externo.com', '123456', 'INVITADO', 'EXTERNO', 1, 'PERU', 'EXTERNO', 'ACTIVO'),
            (16, 'Usuario Inactivo', 'inactivo@techcorp.com', '123456', 'EMPLEADO', 'FINANZAS', 2, 'PERU', 'INTERNO', 'INACTIVO')
        ]
        cursor.executemany('''
            INSERT INTO usuarios (id, nombre, correo, password, rol, departamento, nivel_seguridad, pais, tipo_contrato, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', usuarios)

    # Poblado inicial de documentos de prueba
    cursor.execute("SELECT COUNT(*) FROM documentos")
    if cursor.fetchone()[0] == 0:
        documentos = [
            (501, 'Presupuesto 2027', 'Documento de presupuesto anual', 25, 'FINANZAS', 3, 'PENDIENTE', 'PERU'),
            (502, 'Presupuesto Corporativo', 'Plan financiero corporativo', 12, 'FINANZAS', 4, 'PENDIENTE', 'PERU'),
            (503, 'Manual de Contratación', 'Politicas de RRHH', 11, 'RRHH', 2, 'PUBLICADO', 'PERU'),
            (504, 'Estrategia Secreta 2027', 'Documento altamente confidencial', 13, 'TI', 5, 'PENDIENTE', 'PERU'),
            (505, 'Anuncio Público', 'Comunicado oficial', 13, 'TI', 1, 'PUBLICADO', 'PERU')
        ]
        cursor.executemany('''
            INSERT INTO documentos (id, titulo, descripcion, propietario, departamento, nivel_confidencialidad, estado, pais)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', documentos)

    conn.commit()
    conn.close()