from App import db,app
import App
from App.models.pessoas import Pessoas
from App.models.usuarios import Usuarios,SchemaUsuarios
from App.views.Pessoas import pessoas
from flask import jsonify,request,render_template,redirect,url_for
from sqlalchemy import or_
from flask_login import LoginManager, login_required,logout_user,login_user
from App.views.Auth import helper

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Usuarios.query.get(int(id))

# login 
def login():
    if request.method == 'POST':
        username, senha = request.form['username'],request.form['password']
        usuario = capturaUsuarioPorUserNameEmail(username,username)
        validaSenha = False
         
        if usuario:
           validaSenha = usuario.getValidacaoSenha(senha)

        token = None
        if validaSenha :
            token = helper.getTokenUser(usuario) 
        else:
            return render_template('layouts/login.html',
                                   login=False,
                                   mensagem='Senha não confere.')
        if token:
            usuario.token = token
            db.session.commit()
            login_user(usuario)
        else:
            return render_template('layouts/login.html',
                                   login=False,
                                   mensagem='Houve um erro na geração do Token.')

        return redirect(url_for('index.root',token=token))

# logout      
@login_required      
def logout():
    logout_user()
    redirect(url_for('index.root'))


#captura todos os usuários
def capturaTodosUsuarios():
    usuarios = Usuarios.query.all()
    if usuarios:
        schema = SchemaUsuarios(many=True,exclude=('senha','token'))
        schema = schema.dump(usuarios)
        return jsonify({'data':schema})
    return jsonify({'data':{},'mensagem':'Nenhum Usuário Cadastrado'})

# Captura usuário pelo username
def capturaUsuarioPorUserName(nome):
    condicao = or_(Usuarios.username==nome)
    usuario = Usuarios.query.filter(condicao).\
        join(Pessoas,Pessoas.id==Usuarios.idpessoa).first()
    return usuario


# captura por username e email
def capturaUsuarioPorUserNameEmail(nome,email):
    condicao = or_(Usuarios.username == nome,Pessoas.emailprincipal == email)
    return Usuarios.query.filter(condicao)\
        .join(Pessoas,Pessoas.id==Usuarios.idpessoa).first()

# Gravar novo Usuário
def GravaNovoUsuarioForm():
    from werkzeug.security import generate_password_hash
    if request.method == 'POST':
        data = request.form
        usuario = Usuarios()
        usuario.username = data['username']
        usuario.senha = generate_password_hash(data['senha'])

        # validando username
        if capturaUsuarioPorUserName(usuario.username):
            return jsonify({'mensagem':f'Usuário ja encontra-ser cadastrado com o username: \
                            <strong>{usuario.username}</strong> no sistema',
                            'sucesso': False})
        # validando email
        pessoa = pessoas.getPessoaPorEmail(data['email'])
        if pessoa:
            return jsonify({'mensagem':f'Usuário ja encontra-ser cadastrado com o email:\
                            <strong> {data["email"]} </strong> no sistema',
                            'sucesso': False})

        # validando username
        pessoa = pessoas.getPessoaPorCNPJCPF(data['cnpjcpf'])
        if pessoa:
            return jsonify({'mensagem':f'Usuário ja encontra-ser cadastrado com o CPF/CNPJ: {data["cnpjcpf"]} no sistema',
                            'sucesso': False})
        IdPessoa = pessoas.SalvarNovaPessoa(data)

        if IdPessoa[0] == -1:
            print(IdPessoa[1])
            return jsonify({'mensagem':f' Houve um Erro:{IdPessoa[1]} ao tentar gravar no banco de dados. Tente novamente!',
                            'sucesso': False})
        usuario.idpessoa = IdPessoa[0]
        try:
            db.session.add(usuario)
            db.session.commit()
            return jsonify({'mensagem':f'Usuário {data["username"]} adicionado com sucesso. Faça o Login!',
                        'sucesso':True,'email':data["email"]})
        except Exception as e:
            return jsonify({'mensagem': f' Houve um Erro:{str(e)} ao tentar gravar no banco de dados. Tente novamente!',
                            'sucesso': False})
