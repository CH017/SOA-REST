import logging
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import mysql.connector

# ============================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',      
    'password': '',      
    'database': ''
}

# ============================
# XML DEL MODELO ALUMNO
# ============================
class Alumno(ComplexModel):
    Id_Alumno = Integer
    Matricula = Integer
    Nombre = Unicode
    Apellido_Paterno = Unicode
    Apellido_Materno = Unicode
    Email = Unicode
    Estatus = Unicode

# ============================
# SERVICIO SOAP
# ============================
class AlumnosService(ServiceBase):

    # ============================
    # CREATE
    # ============================
    @rpc(Integer, Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def crear_alumno(ctx, matricula, nombre, apellido_paterno, apellido_materno, email, estatus):

        if estatus not in ["Activo", "Inactivo"]:
            return "Error: Estatus debe ser 'Activo' o 'Inactivo'."

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            query = """
                INSERT INTO alumnos 
                (matricula, nombre, apellido_paterno, apellido_materno, email, estatus)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (matricula, nombre, apellido_paterno, apellido_materno, email, estatus))
            conn.commit()

            return f"Éxito: Alumno {nombre} registrado correctamente."

        except mysql.connector.Error as err:
            return f"Error de BD: {err}"

        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()


    # ============================
    # READ: Lista todos los alumnos
    # ============================
    @rpc(_returns=Array(Alumno))
    def obtener_alumnos(ctx):
        resultados = []
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""SELECT 
                Id_Alumno, Matricula, Nombre, Apellido_Paterno, Apellido_Materno, Email, Estatus
                FROM alumnos
            """)

            rows = cursor.fetchall()

            for row in rows:
                alumno = Alumno()
                alumno.Id_Alumno = row[0]
                alumno.Matricula = row[1]
                alumno.Nombre = row[2]
                alumno.Apellido_Paterno = row[3]
                alumno.Apellido_Materno = row[4]
                alumno.Email = row[5]
                alumno.Estatus = row[6]
                resultados.append(alumno)

            return resultados

        except Exception as e:
            print(f"Error: {e}")
            return []

        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

# ============================
# CONFIG SOAP + SERVIDOR
# ============================
application = Application(
    [AlumnosService],
    tns='universidad.veracruzana.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':

    port = 8000
    print(f"Servidor SOAP iniciado en http://127.0.0.1:{port}")
    print(f"WSDL disponible en http://127.0.0.1:{port}/?wsdl")

    server = make_server('127.0.0.1', port, wsgi_application)
    server.serve_forever()
