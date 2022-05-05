from App.views.Auth import helper
from flask import Blueprint
rotaauth = Blueprint('rotaauth',__name__)

@rotaauth.route('/autentifica.form/',methods=['POST'])
def autentifica_form():
    return  helper.autentifica_form()