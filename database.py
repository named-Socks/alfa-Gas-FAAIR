import os
import json
import shutil
import subprocess
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import bcrypt


# ----------------------------------------------------------------------
# Funciones de apoyo para fechas y direcciones en las pantallas
# ----------------------------------------------------------------------
def formatear_fecha(valor, formato="%d/%m/%Y"):
    """Convierte una fecha/datetime de MySQL a texto. Si viene vacía devuelve '—'."""
    if not valor:
        return "—"
    if isinstance(valor, str):
        return valor
    return valor.strftime(formato)


def texto_a_fecha(texto):
    """Convierte 'dd/mm/aaaa' a 'aaaa-mm-dd'. Vacío -> None. Inválido -> ValueError."""
    texto = texto.strip()
    if not texto:
        return None
    return datetime.strptime(texto, "%d/%m/%Y").strftime("%Y-%m-%d")


def armar_direccion(calle, num_exterior, colonia):
    """Une calle, número y colonia en un solo texto para mostrar en las tablas."""
    if not calle:
        return "Sin dirección"
    return f"{calle} #{num_exterior}, Col. {colonia}"


# ----------------------------------------------------------------------
# Clase principal de conexión y operaciones con MySQL
# ----------------------------------------------------------------------
class BaseDatosLocal:
    def __init__(self):
        self.host = "localhost"
        self.database = "faair_alfa_gas"
        self.user = "root"
        self.password = ""
        self.ultimo_error = None

        # Carpeta por defecto para guardar respaldos y registro de la última fecha
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.carpeta_respaldos = os.path.join(base_dir, "respaldos_bd")
        os.makedirs(self.carpeta_respaldos, exist_ok=True)
        self.archivo_estado_backup = os.path.join(self.carpeta_respaldos, "ultimo_respaldo.json")

    def conectar(self):
        """Crea y devuelve la conexión a MySQL."""
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
        """Ejecuta consultas SELECT y devuelve una lista de diccionarios."""
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
                print(f"Error en consulta SELECT: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()
        return []

    def ejecutar(self, query, parametros=None):
        """Ejecuta comandos INSERT, UPDATE o DELETE."""
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
                print(f"Error al ejecutar instrucción DML: {e}")
                conexion.rollback()
                return None
            finally:
                cursor.close()
                conexion.close()
        return None

    def _comprobar_password(self, contrasena_plana, pass_bd):
        """Compara una contraseña escrita contra texto plano o hash bcrypt."""
        pass_bd = pass_bd or ""
        if pass_bd.startswith("$2"):
            try:
                return bcrypt.checkpw(
                    contrasena_plana.encode("utf-8"),
                    pass_bd.encode("utf-8")
                )
            except ValueError:
                return False
        return contrasena_plana == pass_bd

    def verificar_login(self, usuario, contrasena_plana):
        """Valida usuario y contraseña (soporta texto plano de prueba o hash bcrypt)."""
        query = """
            SELECT id_adm, id_adm AS id_administrador,
                   nombre_adm, nombre_adm AS nombre_completo,
                   nombre_usuario_adm, id_sucursal, password
            FROM administrador
            WHERE nombre_usuario_adm = %s AND activo_adm = 1
        """
        resultado = self.consultar(query, (usuario,))

        if resultado:
            fila = resultado[0]
            if self._comprobar_password(contrasena_plana, fila["password"]):
                return True, fila
        return False, None

    def obtener_info_admin(self, identificador):
        """Obtiene id_adm, nombre_adm y nombre_usuario_adm del administrador activo."""
        if not identificador:
            return None
        query = """
            SELECT id_adm, nombre_adm, nombre_usuario_adm
            FROM administrador
            WHERE activo_adm = 1 AND (nombre_adm = %s OR nombre_usuario_adm = %s)
            LIMIT 1
        """
        resultado = self.consultar(query, (identificador, identificador))
        return resultado[0] if resultado else None

    def cambiar_contrasena_admin(self, identificador, contrasena_actual, contrasena_nueva):
        """Verifica la contraseña actual y guarda la nueva encriptada con bcrypt."""
        conexion = self.conectar()
        if not conexion:
            return False, "No se pudo conectar a la base de datos."

        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id_adm, password
                FROM administrador
                WHERE activo_adm = 1 AND (nombre_adm = %s OR nombre_usuario_adm = %s)
                LIMIT 1
                """,
                (identificador, identificador)
            )
            admin = cursor.fetchone()
            if not admin:
                return False, "No se encontró el usuario administrador en la base de datos."

            if not self._comprobar_password(contrasena_actual, admin["password"]):
                return False, "La contraseña actual es incorrecta."

            if contrasena_actual == contrasena_nueva:
                return False, "La nueva contraseña debe ser diferente a la actual."

            nuevo_hash = bcrypt.hashpw(
                contrasena_nueva.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            cursor.execute(
                "UPDATE administrador SET password = %s WHERE id_adm = %s",
                (nuevo_hash, admin["id_adm"])
            )
            conexion.commit()
            return True, "La contraseña se actualizó correctamente."
        except Error as e:
            conexion.rollback()
            return False, f"Error al actualizar la contraseña en MySQL: {e}"
        finally:
            cursor.close()
            conexion.close()

    def obtener_precio_vigente(self):
        """Devuelve el precio vigente por litro de gas (fecha_fin NULL) o None."""
        query = """
            SELECT pp.precio_producto
            FROM precio_producto pp
            JOIN producto pr ON pr.id_producto = pp.id_producto
            WHERE pr.tipo_producto = 'GAS_ESTACIONARIO' AND pp.fecha_fin IS NULL
            ORDER BY pp.fecha_inicio DESC, pp.id_precio DESC
            LIMIT 1
        """
        resultado = self.consultar(query)
        return resultado[0]["precio_producto"] if resultado else None

    def actualizar_precio_gas(self, nuevo_precio, nombre_admin=None):
        """Cierra el precio vigente anterior y registra el nuevo precio por litro."""
        conexion = self.conectar()
        if not conexion:
            return False, "No se pudo conectar a la base de datos."

        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id_producto FROM producto WHERE tipo_producto = 'GAS_ESTACIONARIO' AND activo_producto = 1 LIMIT 1"
            )
            prod = cursor.fetchone()
            if not prod:
                return False, "No se encontró el producto de Gas LP Estacionario en la base de datos."
            id_producto = prod["id_producto"]

            id_adm = None
            if nombre_admin:
                cursor.execute(
                    "SELECT id_adm FROM administrador WHERE nombre_adm = %s LIMIT 1",
                    (nombre_admin,)
                )
                adm = cursor.fetchone()
                if adm:
                    id_adm = adm["id_adm"]

            # Cerrar precio anterior para conservar historial
            cursor.execute(
                "UPDATE precio_producto SET fecha_fin = CURDATE() WHERE id_producto = %s AND fecha_fin IS NULL",
                (id_producto,)
            )

            # Registrar el nuevo precio vigente
            cursor.execute(
                """
                INSERT INTO precio_producto (id_producto, precio_producto, fecha_inicio, fecha_fin, id_adm)
                VALUES (%s, %s, CURDATE(), NULL, %s)
                """,
                (id_producto, nuevo_precio, id_adm)
            )
            conexion.commit()
            return True, f"El nuevo precio de ${nuevo_precio:.2f} por litro quedó guardado."
        except Error as e:
            conexion.rollback()
            return False, f"Error al guardar el precio en MySQL: {e}"
        finally:
            cursor.close()
            conexion.close()

    # ------------------------------------------------------------------
    # Respaldo manual de la base de datos
    # ------------------------------------------------------------------
    def _buscar_mysqldump(self):
        """Busca mysqldump o mariadb-dump en Linux o XAMPP."""
        for herramienta in ("mysqldump", "mariadb-dump"):
            ruta = shutil.which(herramienta)
            if ruta:
                return ruta
        for ruta_xampp in ("/opt/lampp/bin/mysqldump", "/opt/lampp/bin/mariadb-dump"):
            if os.path.exists(ruta_xampp):
                return ruta_xampp
        return None

    def generar_respaldo(self, ruta_destino):
        """Genera un respaldo .sql completo (tablas, datos y triggers) en la ruta elegida."""
        mysqldump = self._buscar_mysqldump()
        if not mysqldump:
            return False, "No se encontró 'mysqldump' ni 'mariadb-dump' en la computadora."

        comando = [
            mysqldump,
            f"-h{self.host}",
            f"-u{self.user}",
            "--triggers",
            "--single-transaction",
            self.database,
        ]
        if self.password:
            comando.insert(3, f"-p{self.password}")

        try:
            with open(ruta_destino, "w", encoding="utf-8") as archivo_sql:
                resultado = subprocess.run(
                    comando,
                    stdout=archivo_sql,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )

            if resultado.returncode != 0:
                if os.path.exists(ruta_destino):
                    os.remove(ruta_destino)
                return False, f"Error de MySQL al respaldar:\n{resultado.stderr}"

            fecha_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            with open(self.archivo_estado_backup, "w", encoding="utf-8") as f:
                json.dump({"fecha": fecha_str, "archivo": ruta_destino}, f, ensure_ascii=False, indent=2)

            return True, ruta_destino
        except Exception as e:
            if os.path.exists(ruta_destino):
                os.remove(ruta_destino)
            return False, f"Error inesperado al crear el respaldo: {e}"

    def obtener_fecha_ultimo_respaldo(self):
        """Devuelve la fecha del último respaldo guardado o None si aún no hay."""
        if os.path.exists(self.archivo_estado_backup):
            try:
                with open(self.archivo_estado_backup, "r", encoding="utf-8") as f:
                    return json.load(f).get("fecha")
            except Exception:
                return None
        return None