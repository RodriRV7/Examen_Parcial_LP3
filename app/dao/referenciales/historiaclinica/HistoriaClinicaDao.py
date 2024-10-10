from flask import current_app as app
from app.conexion.Conexion import Conexion

class HistoriaClinicaDao:

    def getHistorias(self):
        historiaSQL = """
        SELECT id, paciente_id, descripcion, fecha
        FROM historia_clinica
        """
        # Objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(historiaSQL)
            historias = cur.fetchall()  # Trae todos los datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': historia[0], 'paciente_id': historia[1], 'descripcion': historia[2], 'fecha': historia[3]} for historia in historias]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las historias clínicas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getHistoriaById(self, id):
        historiaSQL = """
        SELECT id, paciente_id, descripcion, fecha
        FROM historia_clinica WHERE id=%s
        """
        # Objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(historiaSQL, (id,))
            historiaEncontrada = cur.fetchone()  # Obtener una sola fila

            if historiaEncontrada:
                return {
                    "id": historiaEncontrada[0],
                    "paciente_id": historiaEncontrada[1],
                    "descripcion": historiaEncontrada[2],
                    "fecha": historiaEncontrada[3]
                }  # Retornar los datos de la historia clínica
            else:
                return None  # Retornar None si no se encuentra la historia

        except Exception as e:
            app.logger.error(f"Error al obtener historia clínica: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarHistoria(self, paciente_id, descripcion, fecha):
        insertHistoriaSQL = """
        INSERT INTO historia_clinica(paciente_id, descripcion, fecha) 
        VALUES(%s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertHistoriaSQL, (paciente_id, descripcion, fecha))
            historia_id = cur.fetchone()[0]  # Obtener el ID generado
            con.commit()  # Confirmar la inserción
            return historia_id

        except Exception as e:
            app.logger.error(f"Error al insertar historia clínica: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateHistoria(self, id, paciente_id, descripcion, fecha):
        updateHistoriaSQL = """
        UPDATE historia_clinica
        SET paciente_id=%s, descripcion=%s, fecha=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateHistoriaSQL, (paciente_id, descripcion, fecha, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar historia clínica: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteHistoria(self, id):
        deleteHistoriaSQL = """
        DELETE FROM historia_clinica
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteHistoriaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar historia clínica: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
