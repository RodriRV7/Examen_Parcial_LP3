# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TratamientoDao:

    def getTratamientos(self):
        tratamientoSQL = """
        SELECT id, nombre, descripcion
        FROM tratamientos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tratamientoSQL)
            tratamientos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': tratamiento[0], 'nombre': tratamiento[1], 'descripcion': tratamiento[2]} for tratamiento in tratamientos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los tratamientos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTratamientoById(self, id):
        tratamientoSQL = """
        SELECT id, nombre, descripcion
        FROM tratamientos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tratamientoSQL, (id,))
            tratamientoEncontrado = cur.fetchone()  # Obtener una sola fila
            if tratamientoEncontrado:
                return {
                    "id": tratamientoEncontrado[0],
                    "nombre": tratamientoEncontrado[1],
                    "descripcion": tratamientoEncontrado[2]
                }  # Retornar los datos del tratamiento
            else:
                return None  # Retornar None si no se encuentra el tratamiento
        except Exception as e:
            app.logger.error(f"Error al obtener tratamiento: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTratamiento(self, nombre, descripcion):
        insertTratamientoSQL = """
        INSERT INTO tratamientos(nombre, descripcion) VALUES(%s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertTratamientoSQL, (nombre, descripcion))
            tratamiento_id = cur.fetchone()[0]
            con.commit()  # Se confirma la inserción
            return tratamiento_id

        except Exception as e:
            app.logger.error(f"Error al insertar tratamiento: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateTratamiento(self, id, nombre, descripcion):
        updateTratamientoSQL = """
        UPDATE tratamientos
        SET nombre=%s, descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTratamientoSQL, (nombre, descripcion, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar tratamiento: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTratamiento(self, id):
        deleteTratamientoSQL = """
        DELETE FROM tratamientos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTratamientoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar tratamiento: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
