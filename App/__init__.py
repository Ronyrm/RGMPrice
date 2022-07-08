from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
app = Flask(__name__)
db = SQLAlchemy(app,session_options={"autoflush": False})
ma = Marshmallow(app)
migrate = Migrate(app,db)

app.config.from_object('config')

# estabelecendo as rotas
from App.rotas.incRotas import estabeleRotas
db.init_app(app)
estabeleRotas()
db.create_all()

