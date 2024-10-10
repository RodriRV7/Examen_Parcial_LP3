# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class RecetaDao:

    def getRecetas(self):
        recetaSQL = """
        SELECT id, paciente, medico, descripcion, fecha
        FROM recetas
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(recetaSQL)
            recetas = cur.fetchall()  # Traer datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [{'id': receta[0], 'paciente': receta[1], 'medico': receta[2], 'descripcion': receta[3], 'fecha': receta[4]} for receta in recetas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las recetas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getRecetaById(self, id):
        recetaSQL = """
        SELECT id, paciente, medico, descripcion, fecha
        FROM recetas WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(recetaSQL, (id,))
            recetaEncontrada = cur.fetchone()  # Obtener una sola fila
            if recetaEncontrada:
                return {
                    "id": recetaEncontrada[0],
                    "paciente": recetaEncontrada[1],
                    "medico": recetaEncontrada[2],
                    "descripcion": recetaEncontrada[3],
                    "fecha": recetaEncontrada[4]
                }
            else:
                return None  # Retornar None si no se encuentra la receta
        except Exception as e:
            app.logger.error(f"Error al obtener receta: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarReceta(self, paciente, medico, descripcion, fecha):
        insertRecetaSQL = """
        INSERT INTO recetas(paciente, medico, descripcion, fecha) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertRecetaSQL, (paciente, medico, descripcion, fecha))
            receta_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return receta_id

        except Exception as e:
            app.logger.error(f"Error al insertar receta: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateReceta(self, id, paciente, medico, descripcion, fecha):
        updateRecetaSQL = """
        UPDATE recetas
        SET paciente=%s, medico=%s, descripcion=%s, fecha=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateRecetaSQL, (paciente, medico, descripcion, fecha, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar receta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteReceta(self, id):
        deleteRecetaSQL = """
        DELETE FROM recetas
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteRecetaSQL, (id,))
            rows_affected = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar receta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
