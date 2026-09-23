from flask import Flask

app = Flask(__name__)


@app.route("/")
def inicio():
    return """
    <h1>🔐 SecureDocs</h1>
    <h2>Sistema de Gestión de Expedientes</h2>
    <p>RBAC + ABAC</p>
    <p>Aplicación funcionando correctamente.</p>
    """


if __name__ == "__main__":
    app.run(debug=True)