db_localhost_postgres ={
    'HOST_POSTGRES' : 'localhost',
    'PORT_POSTGRES' : '5432',
    'PWD_POSTGRES': 'rony1234',
    'USERNAME_POSTGRES': 'postgres',
    'DATABASE_POSTGRES': 'rgmsolutions'
}
# retorna String
def retornaStringConexao(indice):
    if indice == 0:
        return 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_localhost_postgres['USERNAME_POSTGRES'],
                                                                     pw=db_localhost_postgres['PWD_POSTGRES'],
                                                                     url=db_localhost_postgres['HOST_POSTGRES']+':'+
                                                                         db_localhost_postgres['PORT_POSTGRES'],
                                                                     db=db_localhost_postgres['DATABASE_POSTGRES'])

