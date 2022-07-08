from flask import jsonify
from App import db
from App.models.pessoas import Pessoas,SchemaPessoas


def capturaTodosPessoas():
    schema = SchemaPessoas(many=True)
    pessoas = Pessoas.query.all()
    
    return jsonify(schema.dump(pessoas))

def getPessoaPorEmail(email):
    pessoa = Pessoas.query.filter(Pessoas.emailprincipal==email).first()
    return pessoa

def getPessoaPorCNPJCPF(CnpjCpf):
    pessoa = Pessoas.query.filter(Pessoas.cnpjcpf == CnpjCpf).first()
    return pessoa

def SalvarNovaPessoa(data):
    try:
        pessoa = Pessoas()
        pessoa.emailprincipal = data['email']
        pessoa.razaosocial = data['razaosocial']
        pessoa.cnpjcpf = data['cnpjcpf']
        
        pessoa.tipopessoa = 'F' if len(data['cnpjcpf']) == 11 else 'J'
        pessoa.nomefantasia = data['nomefantasia']
        db.session.add(pessoa)
        db.session.commit()
        return [pessoa.id,'']
    except Exception as e:
        return [-1,str(e)]

