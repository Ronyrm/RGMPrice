from App import app
from flask import request,jsonify,render_template,session
from App.views.Pessoas import usuarios
from App.models.usuarios import SchemaUsuarios
from functools import wraps
import jwt

def autentifica_form():
    from werkzeug.security import check_password_hash
    import datetime
    import jwt

    if request.method == 'POST':
        username, senha = request.form['username'],request.form['password']

        usuario = usuarios.capturaUsuarioPorUserNameEmail(username,username)
        if not usuario:
            return render_template('layouts/login.html',
                                   login=False,
                                   mensagem='O Usuário {} não foi encontrado na base de dados.'.format(username))

        valida =  check_password_hash(usuario.senha,senha)
        if not valida:
            return render_template('layouts/login.html',
                                   login=False,
                                   mensagem='Senha não confere.')

        dtexp = datetime.datetime.now() + datetime.timedelta(hours=12)
        token = jwt.encode({'username': usuario.username, 'id': usuario.id, 'exp': dtexp},
                           app.config['SECRET_KEY'],
                           algorithm='HS256')
        try:
            token_decode = token.decode('utf-8')
        except ValueError as err:
            return render_template('layouts/login.html',
                                   login=False,
                                   mensagem='Erro ao decodificar:' + str(err))


        print(token_decode)
        schema = SchemaUsuarios()
        session['current_user'] = schema.dump(usuarios)
        return render_template('layouts/index.html',
                               login=True,
                               mensagem='Usuário logado com sucesso',
                               token=token_decode)

    return jsonify({'mensagem': 'Não pode verificar!', 'login': False}), 401


def token_requerido(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            #return jsonify({'login': False, 'mensagem': ' Token não informado','data': {}}), 401
            return render_template('layouts/login.html',login='',mensagem='')
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = usuarios.capturaUsuarioPorUserName(data['username'])

            #return jsonify({'valide': True, 'mensage': ' Token Valido', 'data': data}), 201

        except:
            return jsonify({'login': False, 'mensagem': ' Token inválido ou expirado', 'data': {}}), 401

        return func(current_user,token,*args, **kwargs)
    return decorated