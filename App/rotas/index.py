from flask import Blueprint,jsonify,render_template,session
from App.models.usuarios import SchemaUsuarios
from App.views.Auth import helper
index = Blueprint('index',__name__)
@index.route('/')
@helper.token_requerido
def root(current_user,token):
    if token:
        return render_template('/layouts/index.html',current_user = current_user, token=token)
    else:
        return render_template('/layouts/login.html',login='',mensagem='')