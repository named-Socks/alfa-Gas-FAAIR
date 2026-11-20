import os
import json
import shutil
import calendar
import subprocess
from datetime import datetime, date
import mysql.connector
from mysql.connector import Error
import bcrypt
import customtkinter as ctk


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
# Selector visual de fecha con calendario desplegable
# ----------------------------------------------------------------------
class _CalendarioPopup(ctk.CTkToplevel):
    """Ventana emergente con calendario mensual para elegir una fecha con un clic."""

    MESES = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    DIAS_SEMANA = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"]

    def __init__(self, parent, fecha_actual, al_seleccionar):
        super().__init__(parent)
        self.al_seleccionar = al_seleccionar
        self.fecha_seleccionada = fecha_actual

        referencia = fecha_actual or date.today()
        self.anio = referencia.year
        self.mes = referencia.month

        self.title("Seleccionar fecha")
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")
        self.transient(parent.winfo_toplevel())
        self.bind("<Escape>", lambda _: self.destroy())

        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=42)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkButton(
            header,
            text="◀",
            width=32,
            height=28,
            fg_color="transparent",
            hover_color="#18321E",
            text_color="#FFFFFF",
            font=("Arial", 13, "bold"),
            command=self._mes_anterior
        ).pack(side="left", padx=6)

        self.lbl_mes_anio = ctk.CTkLabel(
            header,
            text="",
            font=("Arial", 13, "bold"),
            text_color="#FFFFFF"
        )
        self.lbl_mes_anio.pack(side="left", expand=True)

        ctk.CTkButton(
            header,
            text="▶",
            width=32,
            height=28,
            fg_color="transparent",
            hover_color="#18321E",
            text_color="#FFFFFF",
            font=("Arial", 13, "bold"),
            command=self._mes_siguiente
        ).pack(side="right", padx=6)

        dias_header = ctk.CTkFrame(self, fg_color="#F4F6F7", corner_radius=0)
        dias_header.pack(fill="x", padx=8, pady=(8, 2))
        for i, dia_txt in enumerate(self.DIAS_SEMANA):
            dias_header.grid_columnconfigure(i, weight=1, uniform="dias")
            ctk.CTkLabel(
                dias_header,
                text=dia_txt,
                font=("Arial", 11, "bold"),
                text_color="#566573"
            ).grid(row=0, column=i, pady=3)

        self.grid_dias = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_dias.pack(fill="both", expand=True, padx=8, pady=4)
        for i in range(7):
            self.grid_dias.grid_columnconfigure(i, weight=1, uniform="celdas")

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=10, pady=(2, 10))
        footer.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            footer,
            text="Hoy",
            height=28,
            fg_color="#E8F5E9",
            text_color="#214328",
            hover_color="#D5E8D4",
            font=("Arial", 12, "bold"),
            corner_radius=6,
            command=lambda: self._elegir(date.today())
        ).grid(row=0, column=0, padx=(0, 4), sticky="ew")

        ctk.CTkButton(
            footer,
            text="Limpiar",
            height=28,
            fg_color="#F8F9FA",
            text_color="#566573",
            border_width=1,
            border_color="#D5DBDB",
            hover_color="#E9ECEF",
            font=("Arial", 12),
            corner_radius=6,
            command=lambda: self._elegir(None)
        ).grid(row=0, column=1, padx=(4, 0), sticky="ew")

        self._dibujar_mes()
        self.after(40, lambda: self._posicionar(parent))

    def _posicionar(self, widget_origen):
        self.update_idletasks()
        ancho = 272
        alto = 282
        x = widget_origen.winfo_rootx()
        y = widget_origen.winfo_rooty() + widget_origen.winfo_height() + 4

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        if x + ancho > sw:
            x = max(10, sw - ancho - 10)
        if y + alto > sh:
            y = max(10, widget_origen.winfo_rooty() - alto - 4)

        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.grab_set()
        self.focus_set()

    def _mes_anterior(self):
        if self.mes == 1:
            self.mes = 12
            self.anio -= 1
        else:
            self.mes -= 1
        self._dibujar_mes()

    def _mes_siguiente(self):
        if self.mes == 12:
            self.mes = 1
            self.anio += 1
        else:
            self.mes += 1
        self._dibujar_mes()

    def _dibujar_mes(self):
        self.lbl_mes_anio.configure(text=f"{self.MESES[self.mes]} {self.anio}")
        for hijo in self.grid_dias.winfo_children():
            hijo.destroy()

        hoy = date.today()
        semanas = calendar.monthcalendar(self.anio, self.mes)

        for fila_idx, semana in enumerate(semanas):
            for col_idx, dia in enumerate(semana):
                if dia == 0:
                    ctk.CTkLabel(self.grid_dias, text="", height=28).grid(row=fila_idx, column=col_idx, padx=1, pady=1)
                    continue

                fecha_celda = date(self.anio, self.mes, dia)
                es_seleccionada = (self.fecha_seleccionada == fecha_celda)
                es_hoy = (hoy == fecha_celda)

                if es_seleccionada:
                    fg = "#214328"
                    txt_color = "#FFFFFF"
                    hover = "#18321E"
                    borde = 0
                    fuente = ("Arial", 11, "bold")
                elif es_hoy:
                    fg = "#E8F5E9"
                    txt_color = "#214328"
                    hover = "#D5E8D4"
                    borde = 1
                    fuente = ("Arial", 11, "bold")
                else:
                    fg = "transparent"
                    txt_color = "#2C3E50"
                    hover = "#E9ECEF"
                    borde = 0
                    fuente = ("Arial", 11)

                ctk.CTkButton(
                    self.grid_dias,
                    text=str(dia),
                    width=32,
                    height=28,
                    corner_radius=6,
                    fg_color=fg,
                    text_color=txt_color,
                    hover_color=hover,
                    border_width=borde,
                    border_color="#214328",
                    font=fuente,
                    command=lambda f=fecha_celda: self._elegir(f)
                ).grid(row=fila_idx, column=col_idx, padx=1, pady=1, sticky="nsew")

    def _elegir(self, fecha_elegida):
        self.destroy()
        self.al_seleccionar(fecha_elegida)


class SelectorFecha(ctk.CTkFrame):
    """Campo clicable que abre un calendario desplegable y permite limpiar la fecha."""

    def __init__(self, parent, placeholder="Elegir fecha", width=150, on_change=None):
        super().__init__(
            parent,
            fg_color="#F8F9FA",
            corner_radius=8,
            border_width=1,
            border_color="#BDC3C7",
            width=width,
            height=34
        )
        self.pack_propagate(False)
        self.placeholder = placeholder
        self.on_change = on_change
        self._fecha = None
        self._popup = None

        self.btn_fecha = ctk.CTkButton(
            self,
            text=f"📅 {placeholder}",
            fg_color="transparent",
            text_color="#566573",
            hover_color="#E9ECEF",
            font=("Arial", 12),
            anchor="w",
            command=self._abrir_calendario
        )
        self.btn_fecha.pack(side="left", fill="both", expand=True, padx=(3, 0))

        self.btn_limpiar = ctk.CTkButton(
            self,
            text="✕",
            width=22,
            height=22,
            corner_radius=6,
            fg_color="transparent",
            text_color="#7F8C8D",
            hover_color="#FADBD8",
            font=("Arial", 11, "bold"),
            command=self.limpiar
        )

    def _abrir_calendario(self):
        if self._popup is not None and self._popup.winfo_exists():
            self._popup.focus()
            return
        self._popup = _CalendarioPopup(self, self._fecha, self.set_fecha)

    def set_fecha(self, nueva_fecha):
        self._fecha = nueva_fecha
        if nueva_fecha:
            self.btn_fecha.configure(
                text=f"📅 {nueva_fecha.strftime('%d/%m/%Y')}",
                text_color="#214328",
                font=("Arial", 12, "bold")
            )
            self.btn_limpiar.pack(side="right", padx=(0, 3))
        else:
            self.btn_fecha.configure(
                text=f"📅 {self.placeholder}",
                text_color="#566573",
                font=("Arial", 12)
            )
            self.btn_limpiar.pack_forget()

        if self.on_change:
            self.on_change()

    def limpiar(self):
        self.set_fecha(None)

    def get(self):
        return self._fecha.strftime("%d/%m/%Y") if self._fecha else ""


# ----------------------------------------------------------------------
# Clase principal de conexión y operaciones con MySQL (faair_alfa_gas)
# ----------------------------------------------------------------------
class BaseDatosLocal:
    def __init__(self):
        self.host = "localhost"
        self.database = "faair_alfa_gas"
        self.user = "root"
        self.password = ""
        self.ultimo_error = None

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
        """Valida usuario y contraseña del administrador activo."""
        query = """
            SELECT id_adm,
                   nombre_adm,
                   nombre_adm AS nombre_completo,
                   nombre_usuario_adm,
                   id_sucursal,
                   password
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
        """Obtiene datos del administrador activo."""
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
        """Devuelve el precio vigente por litro de Gas LP Estacionario."""
        query = """
            SELECT pp.precio_producto
            FROM precio_producto pp
            JOIN producto pr ON pr.id_producto = pp.id_producto
            WHERE pr.tipo_producto = 'GAS_ESTACIONARIO'
              AND pr.activo_producto = 1
              AND pp.fecha_inicio <= CURDATE()
              AND (pp.fecha_fin IS NULL OR pp.fecha_fin >= CURDATE())
            ORDER BY pp.fecha_inicio DESC, pp.id_precio DESC
            LIMIT 1
        """
        resultado = self.consultar(query)
        return resultado[0]["precio_producto"] if resultado else None

    def actualizar_precio_gas(self, nuevo_precio, nombre_admin=None):
        """Cierra el precio anterior e inserta (o actualiza si es hoy) el nuevo precio vigente."""
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
                    "SELECT id_adm FROM administrador WHERE nombre_adm = %s OR nombre_usuario_adm = %s LIMIT 1",
                    (nombre_admin, nombre_admin)
                )
                adm = cursor.fetchone()
                if adm:
                    id_adm = adm["id_adm"]

            cursor.execute(
                """
                SELECT id_precio FROM precio_producto
                WHERE id_producto = %s AND fecha_inicio = CURDATE() AND fecha_fin IS NULL
                ORDER BY id_precio DESC LIMIT 1
                """,
                (id_producto,)
            )
            hoy_row = cursor.fetchone()

            if hoy_row:
                cursor.execute(
                    """
                    UPDATE precio_producto
                    SET precio_producto = %s, id_adm = %s
                    WHERE id_precio = %s
                    """,
                    (nuevo_precio, id_adm, hoy_row["id_precio"])
                )
            else:
                cursor.execute(
                    """
                    UPDATE precio_producto
                    SET fecha_fin = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
                    WHERE id_producto = %s AND fecha_fin IS NULL
                    """,
                    (id_producto,)
                )
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

    def _buscar_mysqldump(self):
        """Busca mysqldump o mariadb-dump en el sistema o XAMPP."""
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