"""
Flask App
"""

import rq
from flask import Flask
from redis import Redis

from can_mayor.blueprints.arc_archivos.views import arc_archivos
from can_mayor.blueprints.arc_documentos.views import arc_documentos
from can_mayor.blueprints.arc_documentos_bitacoras.views import arc_documentos_bitacoras
from can_mayor.blueprints.arc_documentos_tipos.views import arc_documentos_tipos
from can_mayor.blueprints.arc_juzgados_extintos.views import arc_juzgados_extintos
from can_mayor.blueprints.arc_remesas.views import arc_remesas
from can_mayor.blueprints.arc_remesas_bitacoras.views import arc_remesas_bitacoras
from can_mayor.blueprints.arc_remesas_documentos.views import arc_remesas_documentos
from can_mayor.blueprints.arc_solicitudes.views import arc_solicitudes
from can_mayor.blueprints.arc_solicitudes_bitacoras.views import arc_solicitudes_bitacoras
from can_mayor.blueprints.autoridades.views import autoridades
from can_mayor.blueprints.bitacoras.views import bitacoras
from can_mayor.blueprints.distritos.views import distritos
from can_mayor.blueprints.entradas_salidas.views import entradas_salidas
from can_mayor.blueprints.modulos.views import modulos
from can_mayor.blueprints.permisos.views import permisos
from can_mayor.blueprints.roles.views import roles
from can_mayor.blueprints.sistemas.views import sistemas
from can_mayor.blueprints.tareas.views import tareas
from can_mayor.blueprints.usuarios.models import Usuario
from can_mayor.blueprints.usuarios.views import usuarios
from can_mayor.blueprints.usuarios_roles.views import usuarios_roles
from can_mayor.extensions import csrf, database, login_manager, moment
from config.settings import Settings


def create_app():
    """Crear app"""
    # Definir app
    app = Flask(__name__, instance_relative_config=True)

    # Cargar la configuración
    app.config.from_object(Settings())

    # Redis
    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.task_queue = rq.Queue(app.config["TASK_QUEUE"], connection=app.redis, default_timeout=3000)

    # Registrar blueprints
    app.register_blueprint(arc_archivos)
    app.register_blueprint(arc_documentos)
    app.register_blueprint(arc_documentos_bitacoras)
    app.register_blueprint(arc_documentos_tipos)
    app.register_blueprint(arc_juzgados_extintos)
    app.register_blueprint(arc_remesas)
    app.register_blueprint(arc_remesas_bitacoras)
    app.register_blueprint(arc_remesas_documentos)
    app.register_blueprint(arc_solicitudes)
    app.register_blueprint(arc_solicitudes_bitacoras)
    app.register_blueprint(autoridades)
    app.register_blueprint(bitacoras)
    app.register_blueprint(distritos)
    app.register_blueprint(entradas_salidas)
    app.register_blueprint(modulos)
    app.register_blueprint(permisos)
    app.register_blueprint(roles)
    app.register_blueprint(sistemas)
    app.register_blueprint(tareas)
    app.register_blueprint(usuarios)
    app.register_blueprint(usuarios_roles)

    # Inicializar extensiones
    extensions(app)

    # Inicializar autenticación
    authentication(Usuario)

    # Entregar app
    return app


def extensions(app):
    """Inicializar extensiones"""
    csrf.init_app(app)
    database.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    # socketio.init_app(app)


def authentication(user_model):
    """Inicializar Flask-Login"""
    login_manager.login_view = "usuarios.login"

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)
