# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CitaDao:

    def getCitas(self):
        citaSQL = """
        SELECT id, nombre_paciente, nombre_medico, fecha, hora, motivo
        FROM citas
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(citaSQL)
            citas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{
                'id': cita[0],
                'nombre_paciente': cita[1],
                'nombre_medico': cita[2],
                'fecha': cita[3],
                'hora': cita[4],
                'motivo': cita[5]
            } for cita in citas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las citas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getCitaById(self, id):
        citaSQL = """
        SELECT id, nombre_paciente, nombre_medico, fecha, hora, motivo
        FROM citas WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(citaSQL, (id,))
            citaEncontrada = cur.fetchone()  # Obtener una sola fila
            if citaEncontrada:
                return {
                    "id": citaEncontrada[0],
                    "nombre_paciente": citaEncontrada[1],
                    "nombre_medico": citaEncontrada[2],
                    "fecha": citaEncontrada[3],
                    "hora": citaEncontrada[4],
                    "motivo": citaEncontrada[5]
                }  # Retornar los datos de la cita
            else:
                return None  # Retornar None si no se encuentra la cita
        except Exception as e:
            app.logger.error(f"Error al obtener cita: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCita(self, nombre_paciente, nombre_medico, fecha, hora, motivo):
        insertCitaSQL = """
        INSERT INTO citas(nombre_paciente, nombre_medico, fecha, hora, motivo) VALUES(%s, %s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertCitaSQL, (nombre_paciente, nombre_medico, fecha, hora, motivo))
            cita_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return cita_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar cita: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateCita(self, id, nombre_paciente, nombre_medico, fecha, hora, motivo):
        updateCitaSQL = """
        UPDATE citas
        SET nombre_paciente=%s, nombre_medico=%s, fecha=%s, hora=%s, motivo=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCitaSQL, (nombre_paciente, nombre_medico, fecha, hora, motivo, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar cita: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCita(self, id):
        deleteCitaSQL = """
        DELETE FROM citas
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteCitaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar cita: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
