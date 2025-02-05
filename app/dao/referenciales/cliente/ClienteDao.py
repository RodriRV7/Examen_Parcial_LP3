# Data access object - DAO para Clientes
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ClienteDao:

    def getClientes(self):
        clienteSQL = """
        SELECT id, nombre, direccion, telefono, email
        FROM clientes
        """
        # Objeto de conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(clienteSQL)
            clientes = cur.fetchall()  # Trae los datos de la BD

            # Transformar los datos en una lista de diccionarios
            return [
                {
                    'id': cliente[0],
                    'nombre': cliente[1],
                    'direccion': cliente[2],
                    'telefono': cliente[3],
                    'email': cliente[4]
                }
                for cliente in clientes
            ]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los clientes: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getClienteById(self, id):
        clienteSQL = """
        SELECT id, nombre, direccion, telefono, email
        FROM clientes
        WHERE id=%s
        """
        # Objeto de conexión
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(clienteSQL, (id,))
            clienteEncontrado = cur.fetchone()  # Obtener una sola fila
            if clienteEncontrado:
                return {
                    'id': clienteEncontrado[0],
                    'nombre': clienteEncontrado[1],
                    'direccion': clienteEncontrado[2],
                    'telefono': clienteEncontrado[3],
                    'email': clienteEncontrado[4]
                }  # Retornar los datos del cliente
            else:
                return None  # Retornar None si no se encuentra el cliente

        except Exception as e:
            app.logger.error(f"Error al obtener cliente: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCliente(self, nombre, direccion, telefono, email):
        insertClienteSQL = """
        INSERT INTO clientes (nombre, direccion, telefono, email)
        VALUES (%s, %s, %s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertClienteSQL, (nombre, direccion, telefono, email))
            cliente_id = cur.fetchone()[0]
            con.commit()  # Se confirma la inserción
            return cliente_id

        except Exception as e:
            app.logger.error(f"Error al insertar cliente: {str(e)}")
            con.rollback()  # Retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateCliente(self, id, nombre, direccion, telefono, email):
        updateClienteSQL = """
        UPDATE clientes
        SET nombre=%s, direccion=%s, telefono=%s, email=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateClienteSQL, (nombre, direccion, telefono, email, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()
            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar cliente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCliente(self, id):
        deleteClienteSQL = """
        DELETE FROM clientes
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteClienteSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar cliente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
