# Data Access Object - DAO para la tabla Medicos
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MedicoDao:

    def getMedicos(self):
        medicoSQL = """
        SELECT id, nombre, especialidad, telefono, email
        FROM medicos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(medicoSQL)
            medicos = cur.fetchall()

            # Convertir los resultados en una lista de diccionarios
            return [{
                'id': medico[0],
                'nombre': medico[1],
                'especialidad': medico[2],
                'telefono': medico[3],
                'email': medico[4]
            } for medico in medicos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los médicos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMedicoById(self, id):
        medicoSQL = """
        SELECT id, nombre, especialidad, telefono, email
        FROM medicos WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(medicoSQL, (id,))
            medicoEncontrado = cur.fetchone()

            if medicoEncontrado:
                return {
                    "id": medicoEncontrado[0],
                    "nombre": medicoEncontrado[1],
                    "especialidad": medicoEncontrado[2],
                    "telefono": medicoEncontrado[3],
                    "email": medicoEncontrado[4]
                }
            else:
                return None

        except Exception as e:
            app.logger.error(f"Error al obtener médico: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMedico(self, nombre, especialidad, telefono, email):
        insertMedicoSQL = """
        INSERT INTO medicos(nombre, especialidad, telefono, email) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertMedicoSQL, (nombre, especialidad, telefono, email))
            medico_id = cur.fetchone()[0]
            con.commit()
            return medico_id

        except Exception as e:
            app.logger.error(f"Error al insertar médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateMedico(self, id, nombre, especialidad, telefono, email):
        updateMedicoSQL = """
        UPDATE medicos
        SET nombre=%s, especialidad=%s, telefono=%s, email=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMedicoSQL, (nombre, especialidad, telefono, email, id))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMedico(self, id):
        deleteMedicoSQL = """
        DELETE FROM medicos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMedicoSQL, (id,))
            filas_afectadas = cur.rowcount
            con.commit()

            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar médico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
