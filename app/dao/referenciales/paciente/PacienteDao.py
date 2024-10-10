from flask import current_app as app
from app.conexion.Conexion import Conexion

class PacienteDao:

    def getPacientes(self):
        pacienteSQL = """
        SELECT id, nombre, fecha_nacimiento, telefono, email
        FROM pacientes
        """
        # Objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(pacienteSQL)
            pacientes = cur.fetchall()  # Trae todos los datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': paciente[0], 'nombre': paciente[1], 'fecha_nacimiento': paciente[2], 'telefono': paciente[3], 'email': paciente[4]} for paciente in pacientes]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los pacientes: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPacienteById(self, id):
        pacienteSQL = """
        SELECT id, nombre, fecha_nacimiento, telefono, email
        FROM pacientes WHERE id=%s
        """
        # Objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(pacienteSQL, (id,))
            pacienteEncontrado = cur.fetchone()  # Obtener una sola fila

            if pacienteEncontrado:
                return {
                    "id": pacienteEncontrado[0],
                    "nombre": pacienteEncontrado[1],
                    "fecha_nacimiento": pacienteEncontrado[2],
                    "telefono": pacienteEncontrado[3],
                    "email": pacienteEncontrado[4]
                }  # Retornar los datos del paciente
            else:
                return None  # Retornar None si no se encuentra el paciente

        except Exception as e:
            app.logger.error(f"Error al obtener paciente: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPaciente(self, nombre, fecha_nacimiento, telefono, email):
        insertPacienteSQL = """
        INSERT INTO pacientes(nombre, fecha_nacimiento, telefono, email) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertPacienteSQL, (nombre, fecha_nacimiento, telefono, email))
            paciente_id = cur.fetchone()[0]  # Obtener el ID generado
            con.commit()  # Confirmar la inserción
            return paciente_id

        except Exception as e:
            app.logger.error(f"Error al insertar paciente: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updatePaciente(self, id, nombre, fecha_nacimiento, telefono, email):
        updatePacienteSQL = """
        UPDATE pacientes
        SET nombre=%s, fecha_nacimiento=%s, telefono=%s, email=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePacienteSQL, (nombre, fecha_nacimiento, telefono, email, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar paciente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deletePaciente(self, id):
        deletePacienteSQL = """
        DELETE FROM pacientes
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deletePacienteSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar paciente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
