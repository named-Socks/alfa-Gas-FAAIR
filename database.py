import mysql.connector
from mysql.connector import Error
from datetime import datetime
import bcrypt


# ----------------------------------------------------------------------
# Utilidades pequeñas que usan varias pantallas
# ----------------------------------------------------------------------
def formatear_fecha(valor, formato="%d/%m/%Y"):
    """Convierte una fecha/datetime de MySQL a texto. Si viene vacía devuelve '—'."""
    return valor.strftime(formato) if valor else "—"


def texto_a_fecha(texto):
    """Convierte 'dd/mm/aaaa' a 'aaaa-mm-dd'. Vacío -> None. Inválido -> ValueError."""
    texto = texto.strip()
    if not texto:
        return None
    return datetime.strptime(texto, "%d/%m/%Y").strftime("%Y-%m-%d")


def armar_direccion(calle, num_exterior, colonia, num_interior=None):
    """Une calle, número exterior/interior y colonia en un solo texto para las tablas."""
    if not calle:
        return "Sin dirección"
    numero = f"#{num_exterior}"
    if num_interior:
        numero += f" Int. {num_interior}"
    texto_colonia = f", Col. {colonia}" if colonia else ""
    return f"{calle} {numero}{texto_colonia}"


class BaseDatosLocal:
    def __init__(self):
        # Credenciales de conexión local a MySQL / MariaDB (faair_alfa_gas)
        self.host = "localhost"
        self.database = "faair_alfa_gas"
        self.user = "root"        # Cambia si tu usuario es diferente
        self.password = ""        # Pon tu contraseña de phpMyAdmin/MySQL si tiene
        self.ultimo_error = None  # Guarda el último error de conexión

    def conectar(self):
        """Crea y devuelve la conexión a la base de datos"""
        self.ultimo_error = None
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if conexion.is_connected():
                return conexion
        except Error as e:
            self.ultimo_error = e
            print(f"Error al conectar a MySQL: {e}")
            return None

    def consultar(self, query, parametros=None):
        """Para hacer SELECTS y traer datos como lista de diccionarios"""
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            try:
                if parametros:
                    cursor.execute(query, parametros)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
            except Error as e:
                print(f"Error en consulta: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()
        return []

    def ejecutar(self, query, parametros=None):
        """Para hacer INSERTS, UPDATES y DELETES simples"""
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                if parametros:
                    cursor.execute(query, parametros)
                else:
                    cursor.execute(query)
                conexion.commit()
                return cursor.lastrowid
            except Error as e:
                print(f"Error al ejecutar: {e}")
                conexion.rollback()
                return None
            finally:
                cursor.close()
                conexion.close()
        return None

    # ------------------------------------------------------------------
    # Autenticación y configuración
    # ------------------------------------------------------------------
    def verificar_login(self, usuario, contrasena_plana):
        """Compara la contraseña contra el hash bcrypt (o texto plano) en administrador"""
        query = """
            SELECT id_adm AS id_administrador,
                   nombre_adm AS nombre_completo,
                   id_sucursal,
                   password AS contrasena_hash
            FROM administrador
            WHERE nombre_usuario_adm = %s AND activo_adm = 1
        """
        resultado = self.consultar(query, (usuario,))
        if resultado:
            fila = resultado[0]
            hash_guardado = fila["contrasena_hash"] or ""
            try:
                correcta = bcrypt.checkpw(
                    contrasena_plana.encode("utf-8"),
                    hash_guardado.encode("utf-8")
                )
            except ValueError:
                correcta = (contrasena_plana == hash_guardado)

            if correcta:
                return True, fila
        return False, None

    def obtener_precio_vigente(self):
        """Devuelve el precio vigente por litro de gas (fecha_fin NULL) o None si no hay"""
        query = """
            SELECT pp.precio_producto AS precio
            FROM precio_producto pp
            JOIN producto pr ON pr.id_producto = pp.id_producto
            WHERE pr.tipo_producto = 'GAS_ESTACIONARIO' AND pp.fecha_fin IS NULL
            ORDER BY pp.fecha_inicio DESC
            LIMIT 1
        """
        resultado = self.consultar(query)
        return resultado[0]["precio"] if resultado else None

    # ------------------------------------------------------------------
    # Catálogos de Sucursales y Geografía (entidad, municipio, colonia)
    # ------------------------------------------------------------------
    def obtener_sucursales(self):
        query = """
            SELECT id_sucursal, clave_sucursal, nombre_sucursal
            FROM sucursal
            WHERE activa_sucursal = 1
            ORDER BY nombre_sucursal ASC
        """
        return self.consultar(query)

    def obtener_entidades(self):
        query = """
            SELECT id_entidad_fede, clave_entidad_fede, nombre_entidad_fede
            FROM entidad_federativa
            ORDER BY nombre_entidad_fede ASC
        """
        return self.consultar(query)

    def obtener_municipios(self, id_entidad_fede=None):
        if id_entidad_fede:
            query = """
                SELECT id_municipio, id_entidad_fede, nombre_municipio
                FROM municipio
                WHERE id_entidad_fede = %s
                ORDER BY nombre_municipio ASC
            """
            return self.consultar(query, (id_entidad_fede,))
        query = """
            SELECT id_municipio, id_entidad_fede, nombre_municipio
            FROM municipio
            ORDER BY nombre_municipio ASC
        """
        return self.consultar(query)

    def obtener_colonias(self, id_municipio=None):
        if id_municipio:
            query = """
                SELECT id_colonia, id_municipio, nombre_colonia, codigo_postal
                FROM colonia
                WHERE id_municipio = %s
                ORDER BY nombre_colonia ASC
            """
            return self.consultar(query, (id_municipio,))
        query = """
            SELECT id_colonia, id_municipio, nombre_colonia, codigo_postal
            FROM colonia
            ORDER BY nombre_colonia ASC
        """
        return self.consultar(query)

    # ------------------------------------------------------------------
    # Gestión completa de Clientes (Consulta, Alta y Modificación)
    # ------------------------------------------------------------------
    def obtener_clientes(self, id_sucursal=None, busqueda="", id_entidad=None,
                         id_municipio=None, id_colonia=None, calle=""):
        """Consulta los clientes con su dirección recurrente y predicción vigente"""
        query = """
            SELECT c.id_cliente,
                   c.nombre_cliente,
                   c.telefono_whatsapp_cliente,
                   c.estado_cliente,
                   c.acepta_notificaciones,
                   d.calle,
                   d.num_exterior,
                   d.num_interior,
                   col.nombre_colonia AS colonia,
                   p.promedio_dias_consumo,
                   p.fecha_estimada_agotamiento
            FROM cliente c
            LEFT JOIN direccion d
                   ON d.id_cliente = c.id_cliente AND d.direccion_recurrente_cliente = 1
            LEFT JOIN colonia col ON col.id_colonia = d.id_colonia
            LEFT JOIN municipio m ON m.id_municipio = col.id_municipio
            LEFT JOIN entidad_federativa ef ON ef.id_entidad_fede = m.id_entidad_fede
            LEFT JOIN (
                SELECT id_cliente,
                       MIN(promedio_dias_consumo) AS promedio_dias_consumo,
                       MIN(fecha_estimada_agotamiento) AS fecha_estimada_agotamiento
                FROM prediccion
                WHERE vigente = 1
                GROUP BY id_cliente
            ) p ON p.id_cliente = c.id_cliente
            WHERE (%s IS NULL OR c.id_sucursal = %s)
        """
        params = [id_sucursal, id_sucursal]

        if busqueda:
            query += " AND (c.nombre_cliente LIKE %s OR c.telefono_whatsapp_cliente LIKE %s)"
            params += [f"%{busqueda}%", f"%{busqueda}%"]

        if id_entidad:
            query += " AND ef.id_entidad_fede = %s"
            params.append(id_entidad)

        if id_municipio:
            query += " AND m.id_municipio = %s"
            params.append(id_municipio)

        if id_colonia:
            query += " AND col.id_colonia = %s"
            params.append(id_colonia)

        if calle:
            query += " AND d.calle LIKE %s"
            params.append(f"%{calle}%")

        query += " ORDER BY c.id_cliente DESC"
        return self.consultar(query, params)

    def obtener_cliente_por_id(self, id_cliente):
        """Obtiene toda la información de un cliente y su dirección activa para editarla"""
        query = """
            SELECT c.id_cliente,
                   c.id_sucursal,
                   c.nombre_cliente,
                   c.telefono_whatsapp_cliente,
                   c.estado_cliente,
                   c.acepta_notificaciones,
                   d.id_direccion,
                   d.id_colonia,
                   d.calle,
                   d.num_exterior,
                   d.num_interior,
                   d.referencias,
                   col.nombre_colonia,
                   col.codigo_postal,
                   col.id_municipio,
                   m.nombre_municipio,
                   m.id_entidad_fede,
                   ef.nombre_entidad_fede,
                   s.nombre_sucursal
            FROM cliente c
            LEFT JOIN sucursal s ON s.id_sucursal = c.id_sucursal
            LEFT JOIN direccion d
                   ON d.id_cliente = c.id_cliente AND d.direccion_recurrente_cliente = 1
            LEFT JOIN colonia col ON col.id_colonia = d.id_colonia
            LEFT JOIN municipio m ON m.id_municipio = col.id_municipio
            LEFT JOIN entidad_federativa ef ON ef.id_entidad_fede = m.id_entidad_fede
            WHERE c.id_cliente = %s
        """
        filas = self.consultar(query, (id_cliente,))
        return filas[0] if filas else None

    def registrar_cliente(self, datos_cliente, datos_direccion):
        """Da de alta un cliente nuevo y su dirección recurrente en una sola transacción"""
        conexion = self.conectar()
        if not conexion:
            return False, "No se pudo conectar a la base de datos."

        cursor = conexion.cursor()
        try:
            conexion.start_transaction()

            sql_cliente = """
                INSERT INTO cliente (
                    id_sucursal,
                    nombre_cliente,
                    telefono_whatsapp_cliente,
                    estado_cliente,
                    acepta_notificaciones
                ) VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_cliente, (
                datos_cliente["id_sucursal"],
                datos_cliente["nombre_cliente"],
                datos_cliente["telefono_whatsapp_cliente"],
                datos_cliente["estado_cliente"],
                datos_cliente["acepta_notificaciones"]
            ))
            nuevo_id_cliente = cursor.lastrowid

            sql_direccion = """
                INSERT INTO direccion (
                    id_colonia,
                    id_cliente,
                    direccion_recurrente_cliente,
                    calle,
                    num_exterior,
                    num_interior,
                    referencias
                ) VALUES (%s, %s, 1, %s, %s, %s, %s)
            """
            cursor.execute(sql_direccion, (
                datos_direccion["id_colonia"],
                nuevo_id_cliente,
                datos_direccion["calle"],
                datos_direccion["num_exterior"],
                datos_direccion["num_interior"] or None,
                datos_direccion["referencias"] or None
            ))

            conexion.commit()
            return True, f"Cliente '{datos_cliente['nombre_cliente']}' registrado correctamente (ID #{nuevo_id_cliente})."

        except mysql.connector.IntegrityError as e:
            conexion.rollback()
            if e.errno == 1062:
                return False, "Ya existe un cliente registrado con ese número de WhatsApp."
            return False, f"Error de integridad en los datos: {e}"
        except Error as e:
            conexion.rollback()
            return False, f"Error al guardar el cliente: {e}"
        finally:
            cursor.close()
            conexion.close()

    def actualizar_cliente(self, id_cliente, id_direccion, datos_cliente, datos_direccion):
        """Actualiza los datos personales y la dirección activa de un cliente existente"""
        conexion = self.conectar()
        if not conexion:
            return False, "No se pudo conectar a la base de datos."

        cursor = conexion.cursor()
        try:
            conexion.start_transaction()

            sql_cliente = """
                UPDATE cliente
                SET id_sucursal = %s,
                    nombre_cliente = %s,
                    telefono_whatsapp_cliente = %s,
                    estado_cliente = %s,
                    acepta_notificaciones = %s
                WHERE id_cliente = %s
            """
            cursor.execute(sql_cliente, (
                datos_cliente["id_sucursal"],
                datos_cliente["nombre_cliente"],
                datos_cliente["telefono_whatsapp_cliente"],
                datos_cliente["estado_cliente"],
                datos_cliente["acepta_notificaciones"],
                id_cliente
            ))

            if id_direccion:
                sql_direccion = """
                    UPDATE direccion
                    SET id_colonia = %s,
                        calle = %s,
                        num_exterior = %s,
                        num_interior = %s,
                        referencias = %s
                    WHERE id_direccion = %s AND id_cliente = %s
                """
                cursor.execute(sql_direccion, (
                    datos_direccion["id_colonia"],
                    datos_direccion["calle"],
                    datos_direccion["num_exterior"],
                    datos_direccion["num_interior"] or None,
                    datos_direccion["referencias"] or None,
                    id_direccion,
                    id_cliente
                ))
            else:
                sql_direccion = """
                    INSERT INTO direccion (
                        id_colonia,
                        id_cliente,
                        direccion_recurrente_cliente,
                        calle,
                        num_exterior,
                        num_interior,
                        referencias
                    ) VALUES (%s, %s, 1, %s, %s, %s, %s)
                """
                cursor.execute(sql_direccion, (
                    datos_direccion["id_colonia"],
                    id_cliente,
                    datos_direccion["calle"],
                    datos_direccion["num_exterior"],
                    datos_direccion["num_interior"] or None,
                    datos_direccion["referencias"] or None
                ))

            conexion.commit()
            return True, f"Información del cliente #{id_cliente} actualizada correctamente."

        except mysql.connector.IntegrityError as e:
            conexion.rollback()
            if e.errno == 1062:
                return False, "Ese número de WhatsApp ya pertenece a otro cliente."
            return False, f"Error de integridad en los datos: {e}"
        except Error as e:
            conexion.rollback()
            return False, f"Error al actualizar el cliente: {e}"
        finally:
            cursor.close()
            conexion.close()