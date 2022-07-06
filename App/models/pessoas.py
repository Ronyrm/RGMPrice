from App import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema 

class Pessoas(db.Model):
    __tablename__ = 'pessoas'
    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cnpjcpf        = db.Column(db.String(20), unique=True)
    tipopessoa     = db.Column(db.String(1), nullable=False)
    razaosocial    = db.Column(db.String(100), nullable=False)
    nomefantasia   = db.Column(db.String(100), nullable=False)
    emailprincipal = db.Column(db.String(50), nullable=False, unique=True)
    usuario = db.relationship("Usuarios")

class SchemaPessoas(SQLAlchemyAutoSchema):
    class Meta:
        model: Pessoas
