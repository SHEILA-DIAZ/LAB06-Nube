from flask import Flask, render_template
from flask_cors import CORS
from config.database import init_db
from routes.auth_routes import auth_bp
from routes.documento_routes import doc_bp
from routes.audit_routes import audit_bp

app = Flask(__name__)
CORS(app)

# Inicializar Base de Datos
init_db()

# Registrar Rutas
app.register_blueprint(auth_bp)
app.register_blueprint(doc_bp)
app.register_blueprint(audit_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)