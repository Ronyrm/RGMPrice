from flask import Blueprint,jsonify,render_template,session
from flask_login import login_required,current_user
from App.views.Auth import helper

index = Blueprint('index',__name__)

@index.route('/')
@helper.token_requerido
def root(token):
    
    if token:
        return render_template('/layouts/index.html',current_user=current_user, token=token)
    else:
        return render_template('/layouts/login.html',login='',mensagem='')