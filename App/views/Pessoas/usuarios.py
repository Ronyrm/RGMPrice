from App import db
from App.models.pessoas import Pessoas
from App.models.usuarios import Usuarios,SchemaUsuarios
from App.views.Pessoas import pessoas
from flask import jsonify,request
from sqlalchemy import or_

#captura todos os usuários
def capturaTodosUsuarios():
    usuarios = Usuarios.query.all()
    if usuarios:
        schema = SchemaUsuarios()
        return jsonify({'data':schema.dumps(usuarios,many=True)})
    return jsonify({'data':{},'mensagem':'Nenhum Usuário Cadastrado'})

# Captura usuário pelo username
def capturaUsuarioPorUserNameEmail(nome):
    condicao = or_(Usuarios.username==nome,Pessoas.emailprincipal==nome)
    usuario = Usuarios.query.filter(condicao).\
        join(Pessoas,Pessoas.id==Usuarios.idpessoa).first()
    return usuario

# Gravar novo Usuário
def GravaNovoUsuarioForm():
    if request.method == 'POST':
        data = request.form
        usuario = Usuarios()
        usuario.username = data['username']
        usuario.senha = data['senha']

        # validando username
        if capturaUsuarioPorUserName(usuario.username):
            return jsonify({'mensagem':f'Usuário ja encontra-ser cadastrado com o username: {usuario.username} no sistema',
                            'sucesso': False})
        # validando email
        pessoa = pessoas.getPessoaPorEmail(data['email'])
        if pessoa:
            return jsonify({'mensagem':f'Usuário ja encontra-ser cadastrado com o email: {data["email"]} no sistema',
                            'sucesso': False})

        # validando username
        pessoa = pessoas.getPessoaPorCNPJCPF(data['cnpjcpf'])
        if pessoa:
            return jsonify({'mensagem':f'Usuário ja encontra-ser cadastrado com o CPF/CNPJ: {data["cnpjcpf"]} no sistema',
                            'sucesso': False})
        IdPessoa = pessoas.SalvarNovaPessoa(data)

        if IdPessoa == -1:
            return jsonify({'mensagem':f' Houve um Erro ao tentar gravar no banco de dados. Tente novamente!',
                            'sucesso': False})
        usuario.idpessoa = IdPessoa
        try:
            db.session.add(usuario)
            db.commit()
            return jsonify({'mensagem':f'Usuário {data["username"]} adicionado com sucesso',
                        'sucesso':True})
        except:
            return jsonify({'mensagem': f' Houve um Erro ao tentar gravar no banco de dados. Tente novamente!',
                            'sucesso': False})
