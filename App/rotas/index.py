from flask import Blueprint,jsonify,render_template,session
from flask_login import login_required
from App.models.usuarios import SchemaUsuarios
from App.views.Auth import helper
from App.views.Pessoas import usuarios
index = Blueprint('index',__name__)
@login_required
@index.route('/')

@helper.token_requerido
def root(current_user,token):
    print(usuarios.load_user)
    print(session['current_user'])
    if token:
        return render_template('/layouts/index.html',current_user = current_user, token=token)
    else:
        return render_template('/layouts/login.html',login='',mensagem='')