import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from insert_data import estoy_en_insert
class DataBaseCountry:
    def __init__(self):
        load_dotenv()
        host = os.getenv("HOST")
        port = os.getenv("PORT")
        user = os.getenv("USER")
        psw = os.getenv("PASSWORD")
        database = os.getenv("DATABASE")
        self.conn: mysql = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password= psw,
            database= database,
        )

    def get_connection(self):
        try:
            if self.conn.is_connected():
                print("Conexion establecida...")
                info_server = self.conn.get_server_info()
                print("Informaciond el servido: ", info_server)
                # comprobar que la db exista
                cursor = self.conn.cursor()
                cursor.execute("show tables like 'paises_del_mundo'")
                result = cursor.fetchone()
                if result:
                    print("la tabla 'paises_del_mundo' exite")
                    estoy_en_insert()
                else:
                    print("La tabla no existe 'paises_del_mundo'. Creando tabla...")
                    self.creating_table()
        except Error as err:
            print("Error a la hora de realizar la conexion con bases de datos : {0}".format(err))
            return None

    def creating_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS paises_del_mundo(
                    _id INT AUTO_INCREMENT PRIMARY KEY,
                    p_pais VARCHAR(50),
                    p_nombre VARCHAR(50),
                    p_poblacion INT(50),
                    p_area FLOAT(50)
                )
            ''')
            print("\nTabla 'paises_del_mundo' creada exitosamente.\n")

            # comprobamos los datos en la tabla de la base de datos
            cursor.execute('SELECT COUNT(*) FROM paises_del_mundo')
            total_count = cursor.fetchone()[0]
            print(f'Total records in paises_del_mundo table: {total_count}')
        except Error as ex:
            print("Error al crear la tabla:", ex)

if __name__ == '__main__':
    db: DataBaseCountry = DataBaseCountry()
    db.get_connection()