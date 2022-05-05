from flask import Blueprint
from App.views.Pessoas import usuarios

rotausers = Blueprint('rotausers',__name__)

# captura todos usuários
@rotausers.route('/get/usuarios/all')
def capturaTodosUsuarios():
    return usuarios.capturaTodosUsuarios()
def gravaNovoUsuario():
    return usuarios.GravaNovoUsuarioForm()