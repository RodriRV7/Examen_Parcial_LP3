from flask import current_app as app
from app.conexion.Conexion import Conexion

class DiagnosticoDao:

    def getDiagnosticos(self):

        diagnosticoSQL = """
        SELECT id, nombre, descripcion
        FROM diagnosticos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(diagnosticoSQL)
            diagnosticos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': diag[0], 'nombre': diag[1], 'descripcion': diag[2]} for diag in diagnosticos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los diagnósticos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDiagnosticoById(self, id):

        diagnosticoSQL = """
        SELECT id, nombre, descripcion
        FROM diagnosticos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(diagnosticoSQL, (id,))
            diagnosticoEncontrado = cur.fetchone()  # Obtener una sola fila
            if diagnosticoEncontrado:
                return {
                    "id": diagnosticoEncontrado[0],
                    "nombre": diagnosticoEncontrado[1],
                    "descripcion": diagnosticoEncontrado[2]
                }  # Retornar los datos del diagnóstico
            else:
                return None  # Retornar None si no se encuentra el diagnóstico

        except Exception as e:
            app.logger.error(f"Error al obtener diagnóstico: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDiagnostico(self, nombre, descripcion):

        insertDiagnosticoSQL = """
        INSERT INTO diagnosticos(nombre, descripcion) VALUES(%s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertDiagnosticoSQL, (nombre, descripcion))
            diagnostico_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return diagnostico_id

        # Si algo falló entra aquí
        except Exception as e:
            app.logger.error(f"Error al insertar diagnóstico: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va a ejecutar
        finally:
            cur.close()
            con.close()

    def updateDiagnostico(self, id, nombre, descripcion):

        updateDiagnosticoSQL = """
        UPDATE diagnosticos
        SET nombre=%s, descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDiagnosticoSQL, (nombre, descripcion, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar diagnóstico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDiagnostico(self, id):

        deleteDiagnosticoSQL = """
        DELETE FROM diagnosticos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteDiagnosticoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar diagnóstico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
