from App.conexao.configDB import retornaStringConexao
from App.funcoes.geradorSenhaseKeys import  getKey

SQLALCHEMY_DATABASE_URI = retornaStringConexao(0)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = getKey()

DEBUG = True

