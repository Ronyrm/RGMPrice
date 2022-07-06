from App import db
from datetime import datetime
from App.models.pessoas import SchemaPessoas
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from marshmallow import fields

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    datacriacao = db.Column(db.DateTime, default=datetime.now())
    idpessoa = db.Column(db.Integer, db.ForeignKey('pessoas.id',back_populates="usuario"))
    pessoa = db.relationship("Pessoas")
    
class SchemaUsuarios(SQLAlchemyAutoSchema):
    class Meta:
        model: Usuarios
    pessoa = fields.Nested(SchemaPessoas)