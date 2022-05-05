from App import db
from App.models.pessoas import Pessoas


def getPessoaPorEmail(email):
    pessoa = Pessoas.query(Pessoas.emailprincipal==email).First()
    return pessoa

def getPessoaPorCNPJCPF(CnpjCpf):
    pessoa = Pessoas.query(Pessoas.cnpjcpf == CnpjCpf).First()
    return pessoa

def SalvarNovaPessoa(data):
    try:
        pessoa = Pessoas()
        pessoa.emailprincipal = data['email']
        pessoa.razaosocial = data['nome']
        pessoa.cnpjcpf = data['cnpjcpf']
        pessoa.tipopessoa = data['tipopessoa']
        pessoa.nomefantasia = data['nomefantasia']

        db.session.add(pessoa)
        db.commit()
        return pessoa.id
    except:
        return -1

