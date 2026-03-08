import aiomysql  # Libreria para trabajar con MySQL async

# Configuración de la base de datos MySQL
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "user",
    "password": "123",
    "db": "citas_db"
}


# funcion que permite la conexion a la base de datos

async def get_connection():
    """"
    Establece una conexión a la base de datos MySQL utilizando aiomysql.
    """
    return await aiomysql.connect(**DB_CONFIG) # Desempaqueta la configuración de la base de datos y establece la conexión