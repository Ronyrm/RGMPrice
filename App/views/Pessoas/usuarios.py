from App import db,app
from App.models.pessoas import Pessoas
from App.models.usuarios import Usuarios,SchemaUsuarios
from App.views.Pessoas import pessoas
from flask import jsonify,request
from sqlalchemy import or_
from flask_login import LoginManager,logout_user,login_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Usuarios.query.get(int(id))

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
