from flask import Blueprint
from App.views.Pessoas import pessoas

rotapessoas = Blueprint('rotapessoas',__name__)

# captura todos usuários
@rotapessoas.route('/get/pessoas/all')
def capturaTodasPessoas():
    return pessoas.capturaTodosPessoas()
