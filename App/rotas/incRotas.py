from App import app
def estabeleRotas():

    # Rota Principal
    from App.rotas.index import index
    app.register_blueprint(index)

    # Rotas Usuarios
    from App.rotas.Pessoas.usuarios import rotausers
    app.register_blueprint(rotausers)

    #Rotas Autentificação
    from App.rotas.autentifica import rotaauth
    app.register_blueprint(rotaauth)
