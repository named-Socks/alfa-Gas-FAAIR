import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
from database import formatear_fecha, armar_direccion


class ModalEditarCliente(ctk.CTkToplevel):
    """Ventana emergente para registrar un cliente nuevo o editar uno existente."""

    def __init__(self, parent, db, datos_cliente, colonias_map, al_guardar, id_sucursal=None):
        super().__init__(parent)
        self.db = db
        self.datos_cliente = datos_cliente or {}
        self.es_nuevo = datos_cliente is None
        self.colonias_map = colonias_map
        self.al_guardar = al_guardar
        self.id_sucursal = id_sucursal

        self.title("Nuevo cliente - Alfa Gas" if self.es_nuevo else "Editar cliente - Alfa Gas")
        self.geometry("540x670")
        self.resizable(False, False)
        self.configure(fg_color="#F4F6F7")
        self.transient(parent.winfo_toplevel())
        self.bind("<Escape>", lambda _: self.destroy())

        # Barra superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=76)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        titulo_modal = "➕  Nuevo cliente" if self.es_nuevo else "✏️  Editar cliente"
        ctk.CTkLabel(
            header,
            text=titulo_modal,
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=24)

        # Contenedor blanco principal
        card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#D5DBDB"
        )
        card.pack(fill="both", expand=True, padx=20, pady=18)

        # Campo: Nombre completo
        ctk.CTkLabel(
            card,
            text="Nombre del cliente",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", padx=24, pady=(18, 4))
        self.entry_nombre = ctk.CTkEntry(
            card,
            height=42,
            font=("Arial", 16),
            corner_radius=8,
            border_color="#BDC3C7"
        )
        self.entry_nombre.pack(fill="x", padx=24)
        self.entry_nombre.insert(0, self.datos_cliente.get("nombre_cliente") or "")

        # Fila: Teléfono + Estatus
        fila_tel_est = ctk.CTkFrame(card, fg_color="transparent")
        fila_tel_est.pack(fill="x", padx=24, pady=(12, 0))
        fila_tel_est.grid_columnconfigure((0, 1), weight=1, uniform="tel_est")

        col_tel = ctk.CTkFrame(fila_tel_est, fg_color="transparent")
        col_tel.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        ctk.CTkLabel(
            col_tel,
            text="Teléfono WhatsApp",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 4))
        self.entry_telefono = ctk.CTkEntry(
            col_tel,
            height=42,
            font=("Arial", 16),
            corner_radius=8,
            border_color="#BDC3C7"
        )
        self.entry_telefono.pack(fill="x")
        self.entry_telefono.insert(0, self.datos_cliente.get("telefono_whatsapp_cliente") or "")

        col_est = ctk.CTkFrame(fila_tel_est, fg_color="transparent")
        col_est.grid(row=0, column=1, padx=(8, 0), sticky="ew")
        ctk.CTkLabel(
            col_est,
            text="Estatus del cliente",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 4))
        estatus_actual = self.datos_cliente.get("estado_cliente") or "ACTIVO"
        self.var_estatus = ctk.StringVar(value=estatus_actual)
        self.menu_estatus = ctk.CTkOptionMenu(
            col_est,
            variable=self.var_estatus,
            values=["ACTIVO", "PENDIENTE_REGISTRO", "INACTIVO", "BAJA"],
            height=42,
            font=("Arial", 15),
            dropdown_font=("Arial", 15),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB"
        )
        self.menu_estatus.pack(fill="x")

        # Separador visual para dirección vigente
        separador = ctk.CTkFrame(card, fg_color="#E5E8E8", height=2)
        separador.pack(fill="x", padx=24, pady=(18, 12))

        ctk.CTkLabel(
            card,
            text="Dirección vigente de entrega",
            font=("Arial", 17, "bold"),
            text_color="#214328"
        ).pack(anchor="w", padx=24, pady=(0, 8))

        # Campo: Colonia
        ctk.CTkLabel(
            card,
            text="Colonia",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", padx=24, pady=(2, 4))

        nombres_colonias = list(colonias_map.keys())
        opciones_colonia = ["Sin colonia"] + nombres_colonias if nombres_colonias else ["Sin colonia"]
        colonia_actual = self.datos_cliente.get("nombre_colonia")
        valor_inicial_col = colonia_actual if colonia_actual in colonias_map else "Sin colonia"

        self.var_colonia = ctk.StringVar(value=valor_inicial_col)
        self.menu_colonia = ctk.CTkOptionMenu(
            card,
            variable=self.var_colonia,
            values=opciones_colonia,
            height=42,
            font=("Arial", 15),
            dropdown_font=("Arial", 15),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB"
        )
        self.menu_colonia.pack(fill="x", padx=24)

        # Fila: Calle + Número exterior
        fila_dir = ctk.CTkFrame(card, fg_color="transparent")
        fila_dir.pack(fill="x", padx=24, pady=(12, 0))
        fila_dir.grid_columnconfigure(0, weight=3)
        fila_dir.grid_columnconfigure(1, weight=1)

        col_calle = ctk.CTkFrame(fila_dir, fg_color="transparent")
        col_calle.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        ctk.CTkLabel(
            col_calle,
            text="Calle",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 4))
        self.entry_calle = ctk.CTkEntry(
            col_calle,
            height=42,
            font=("Arial", 16),
            corner_radius=8,
            border_color="#BDC3C7"
        )
        self.entry_calle.pack(fill="x")
        self.entry_calle.insert(0, self.datos_cliente.get("calle") or "")

        col_num = ctk.CTkFrame(fila_dir, fg_color="transparent")
        col_num.grid(row=0, column=1, padx=(8, 0), sticky="ew")
        ctk.CTkLabel(
            col_num,
            text="Núm. ext.",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 4))
        self.entry_num = ctk.CTkEntry(
            col_num,
            height=42,
            font=("Arial", 16),
            corner_radius=8,
            border_color="#BDC3C7"
        )
        self.entry_num.pack(fill="x")
        self.entry_num.insert(0, str(self.datos_cliente.get("num_exterior") or ""))
        self.entry_num.bind("<Return>", lambda _: self.guardar())

        # Mensaje de validación
        self.lbl_error = ctk.CTkLabel(
            card,
            text="",
            font=("Arial", 14, "bold"),
            text_color="#C0392B",
            wraplength=440,
            justify="center"
        )
        self.lbl_error.pack(pady=(14, 4), padx=20)

        # Botones inferiores
        fila_botones = ctk.CTkFrame(card, fg_color="transparent")
        fila_botones.pack(fill="x", side="bottom", padx=24, pady=(8, 20))
        fila_botones.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            fila_botones,
            text="Cancelar",
            height=44,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            border_width=1,
            border_color="#BDC3C7",
            hover_color="#E9ECEF",
            font=("Arial", 16, "bold"),
            corner_radius=8,
            command=self.destroy
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        texto_btn_guardar = "Registrar cliente" if self.es_nuevo else "Guardar cambios"
        ctk.CTkButton(
            fila_botones,
            text=texto_btn_guardar,
            height=44,
            fg_color="#214328",
            text_color="#FFFFFF",
            hover_color="#18321E",
            font=("Arial", 16, "bold"),
            corner_radius=8,
            command=self.guardar
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.after(60, self._centrar_y_enfocar)

    def _centrar_y_enfocar(self):
        self.update_idletasks()
        master = self.master.winfo_toplevel()
        x = master.winfo_rootx() + (master.winfo_width() - self.winfo_width()) // 2
        y = master.winfo_rooty() + (master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        self.grab_set()
        self.entry_nombre.focus_set()

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        estatus = self.var_estatus.get()
        colonia_sel = self.var_colonia.get()
        calle = self.entry_calle.get().strip()
        num_ext = self.entry_num.get().strip()

        if not nombre:
            self.lbl_error.configure(text="El nombre del cliente no puede quedar vacío.")
            return

        if not telefono:
            self.lbl_error.configure(text="El teléfono de WhatsApp no puede quedar vacío.")
            return

        tiene_datos_dir = bool(calle or num_ext or colonia_sel != "Sin colonia")
        if tiene_datos_dir:
            if colonia_sel == "Sin colonia" or colonia_sel not in self.colonias_map:
                self.lbl_error.configure(text="Selecciona una colonia válida para la dirección.")
                return
            if not calle:
                self.lbl_error.configure(text="Escribe el nombre de la calle.")
                return
            if not num_ext:
                self.lbl_error.configure(text="Escribe el número exterior (o 'S/N').")
                return

        conexion = self.db.conectar()
        if not conexion:
            self.lbl_error.configure(text="No se pudo conectar a la base de datos.")
            return

        cursor = conexion.cursor()
        try:
            if self.es_nuevo:
                id_suc = self.id_sucursal
                if not id_suc:
                    cursor.execute("SELECT id_sucursal FROM sucursal ORDER BY id_sucursal ASC LIMIT 1")
                    fila_suc = cursor.fetchone()
                    id_suc = fila_suc[0] if fila_suc else 1

                cursor.execute(
                    """
                    INSERT INTO cliente (
                        id_sucursal, nombre_cliente, telefono_whatsapp_cliente, estado_cliente
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (id_suc, nombre, telefono, estatus)
                )
                id_cliente = cursor.lastrowid

                if tiene_datos_dir:
                    id_colonia = self.colonias_map[colonia_sel]
                    cursor.execute(
                        """
                        INSERT INTO direccion (
                            id_cliente, id_colonia, calle, num_exterior, direccion_recurrente_cliente
                        )
                        VALUES (%s, %s, %s, %s, 1)
                        """,
                        (id_cliente, id_colonia, calle, num_ext)
                    )

                conexion.commit()
                self.destroy()
                self.al_guardar()
                messagebox.showinfo(
                    "Cliente registrado",
                    f"El cliente {nombre} se registró correctamente."
                )
            else:
                id_cliente = self.datos_cliente["id_cliente"]
                cursor.execute(
                    """
                    UPDATE cliente
                    SET nombre_cliente = %s,
                        telefono_whatsapp_cliente = %s,
                        estado_cliente = %s
                    WHERE id_cliente = %s
                    """,
                    (nombre, telefono, estatus, id_cliente)
                )

                if tiene_datos_dir:
                    id_colonia = self.colonias_map[colonia_sel]
                    id_direccion = self.datos_cliente.get("id_direccion")
                    if id_direccion:
                        cursor.execute(
                            """
                            UPDATE direccion
                            SET calle = %s,
                                num_exterior = %s,
                                id_colonia = %s
                            WHERE id_direccion = %s
                            """,
                            (calle, num_ext, id_colonia, id_direccion)
                        )
                    else:
                        cursor.execute(
                            """
                            INSERT INTO direccion (
                                id_cliente, id_colonia, calle, num_exterior, direccion_recurrente_cliente
                            )
                            VALUES (%s, %s, %s, %s, 1)
                            """,
                            (id_cliente, id_colonia, calle, num_ext)
                        )

                conexion.commit()
                self.destroy()
                self.al_guardar()
                messagebox.showinfo(
                    "Cliente actualizado",
                    f"Los datos de {nombre} se guardaron correctamente."
                )
        except Exception as e:
            conexion.rollback()
            if "Duplicate entry" in str(e):
                self.lbl_error.configure(text="Ya existe un cliente registrado con ese teléfono.")
            else:
                self.lbl_error.configure(text=f"Error al guardar en MySQL: {e}")
        finally:
            cursor.close()
            conexion.close()


class ClientesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._clientes_cache = {}
        self._colonias_map = {}
        self._modal_editar = None

        # Barra superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")

        img_icono = Image.open("/home/jayb/Documentos/GitHub/alfa-Gas-FAAIR/alfaGasIcono.png")
        self.icono_alfa = ctk.CTkImage(light_image=img_icono, dark_image=img_icono, size=(209, 71.33))

        ctk.CTkLabel(
            header,
            image=self.icono_alfa,
            text="   Clientes y predicciones",
            compound="left",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=35, pady=22)

        ctk.CTkButton(
            header,
            text="Regresar a inicio 🏠",
            fg_color="#F8F9FA",
            text_color="#214328",
            hover_color="#E2E6EA",
            font=("Arial", 16, "bold"),
            height=42,
            corner_radius=20,
            command=lambda: self.controller.mostrar_pantalla("menu")
        ).pack(side="right", padx=35)

        self.lbl_admin = ctk.CTkLabel(header, text="", font=("Arial", 16, "bold"), text_color="#FFFFFF")
        self.lbl_admin.pack(side="right", padx=12)

        # Contenedor blanco principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Fila 1: Estatus, historial, búsqueda y nuevo cliente
        top_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(20, 8))

        ctk.CTkLabel(
            top_bar,
            text="Filtros:",
            font=("Arial", 17, "bold"),
            text_color="#2C3E50"
        ).pack(side="left", padx=(0, 12))

        estilo_combo = {
            "height": 44,
            "font": ("Arial", 16),
            "dropdown_font": ("Arial", 16),
            "fg_color": "#F8F9FA",
            "text_color": "#2C3E50",
            "button_color": "#D5DBDB",
        }

        self.var_estado_cli = ctk.StringVar(value="Todos")
        self.menu_estado = ctk.CTkOptionMenu(
            top_bar,
            variable=self.var_estado_cli,
            values=["Todos", "ACTIVO", "PENDIENTE_REGISTRO", "INACTIVO", "BAJA"],
            width=215,
            command=lambda _: self.cargar_datos(),
            **estilo_combo
        )
        self.menu_estado.pack(side="left", padx=(0, 10))

        self.var_historial = ctk.StringVar(value="Historial: Todos")
        self.menu_historial = ctk.CTkOptionMenu(
            top_bar,
            variable=self.var_historial,
            values=["Historial: Todos", "Con predicción", "Sin historial"],
            width=205,
            command=lambda _: self.cargar_datos(),
            **estilo_combo
        )
        self.menu_historial.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            top_bar,
            text="➕ Nuevo cliente",
            fg_color="#214328",
            hover_color="#18321E",
            text_color="#FFFFFF",
            font=("Arial", 16, "bold"),
            height=44,
            corner_radius=10,
            command=self._abrir_modal_nuevo
        ).pack(side="right", padx=(12, 0))

        self.entry_buscar = ctk.CTkEntry(
            top_bar,
            placeholder_text="🔍 Buscar por nombre o teléfono...",
            width=280,
            height=44,
            font=("Arial", 16),
            corner_radius=22
        )
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda _: self.cargar_datos())

        # Fila 2: Filtros geográficos (Estado, Ciudad, Colonia, Calle)
        filtros_geo = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_geo.pack(fill="x", padx=20, pady=(0, 8))

        self.var_entidad = ctk.StringVar(value="Estado: Todos")
        self.menu_entidad = ctk.CTkOptionMenu(
            filtros_geo,
            variable=self.var_entidad,
            values=["Estado: Todos"],
            width=205,
            command=self._al_cambiar_entidad,
            **estilo_combo
        )
        self.menu_entidad.pack(side="left", padx=(0, 10))

        self.var_municipio = ctk.StringVar(value="Ciudad: Todos")
        self.menu_municipio = ctk.CTkOptionMenu(
            filtros_geo,
            variable=self.var_municipio,
            values=["Municipio: Todos"],
            width=215,
            command=self._al_cambiar_municipio,
            **estilo_combo
        )
        self.menu_municipio.pack(side="left", padx=(0, 10))

        self.var_colonia = ctk.StringVar(value="Todas las colonias")
        self.menu_colonia = ctk.CTkOptionMenu(
            filtros_geo,
            variable=self.var_colonia,
            values=["Todas las colonias"],
            width=230,
            command=self._al_cambiar_colonia,
            **estilo_combo
        )
        self.menu_colonia.pack(side="left", padx=(0, 10))

        self.var_calle = ctk.StringVar(value="Calle: Todas")
        self.menu_calle = ctk.CTkOptionMenu(
            filtros_geo,
            variable=self.var_calle,
            values=["Calle: Todas"],
            width=220,
            command=lambda _: self.cargar_datos(),
            **estilo_combo
        )
        self.menu_calle.pack(side="left")

        # Contenedor de tabla con barras de desplazamiento
        tabla_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=15)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal")

        columnas = ("id", "nombre", "telefono", "direccion", "frecuencia", "ultima", "proxima", "estatus", "editar")
        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        encabezados = [
            "ID", "Nombre del cliente", "Teléfono", "Dirección vigente",
            "Frecuencia", "Último pedido", "Próximo estimado", "Estatus", "Editar"
        ]
        anchos = [65, 210, 140, 280, 130, 145, 175, 205, 115]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho, minwidth=ancho)

        self.tabla.bind("<ButtonRelease-1>", self._al_hacer_clic_tabla)
        self.tabla.bind("<Motion>", self._al_mover_mouse_tabla)
        self.tabla.bind("<Double-1>", self._al_doble_clic_tabla)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)

    def _es_columna_editar(self, event):
        if self.tabla.identify_region(event.x, event.y) != "cell":
            return False
        col_id = self.tabla.identify_column(event.x)
        if not col_id or not col_id.startswith("#"):
            return False
        indice = int(col_id[1:]) - 1
        columnas = self.tabla["columns"]
        return 0 <= indice < len(columnas) and columnas[indice] == "editar"

    def _al_mover_mouse_tabla(self, event):
        if self._es_columna_editar(event) and self.tabla.identify_row(event.y):
            self.tabla.configure(cursor="hand2")
        else:
            self.tabla.configure(cursor="")

    def _al_hacer_clic_tabla(self, event):
        if not self._es_columna_editar(event):
            return
        row_id = self.tabla.identify_row(event.y)
        if row_id:
            self.tabla.selection_set(row_id)
            self._abrir_modal_por_id(row_id)

    def _al_doble_clic_tabla(self, _event):
        seleccion = self.tabla.selection()
        if seleccion:
            self._abrir_modal_por_id(seleccion[0])

    def _abrir_modal_nuevo(self):
        if self._modal_editar is not None and self._modal_editar.winfo_exists():
            self._modal_editar.focus()
            return

        self._modal_editar = ModalEditarCliente(
            self,
            db=self.controller.db,
            datos_cliente=None,
            colonias_map=self._colonias_map,
            al_guardar=self.cargar_datos,
            id_sucursal=self.controller.id_sucursal_actual
        )

    def _abrir_modal_por_id(self, id_cliente_str):
        if self._modal_editar is not None and self._modal_editar.winfo_exists():
            self._modal_editar.focus()
            return

        datos_cliente = self._clientes_cache.get(id_cliente_str)
        if not datos_cliente:
            return

        self._modal_editar = ModalEditarCliente(
            self,
            db=self.controller.db,
            datos_cliente=datos_cliente,
            colonias_map=self._colonias_map,
            al_guardar=self.cargar_datos,
            id_sucursal=self.controller.id_sucursal_actual
        )

    def _cargar_colonias(self):
        filas = self.controller.db.consultar(
            "SELECT MIN(id_colonia) AS id_colonia, nombre_colonia FROM colonia GROUP BY nombre_colonia ORDER BY nombre_colonia"
        )
        self._colonias_map = {f["nombre_colonia"]: f["id_colonia"] for f in filas}

    def _cargar_opciones_filtros(self):
        self._cargar_colonias()
        estados = self.controller.db.consultar(
            "SELECT nombre_entidad_fede FROM entidad_federativa ORDER BY nombre_entidad_fede"
        )
        lista_estados = ["Estado: Todos"] + [r["nombre_entidad_fede"] for r in estados]
        self.menu_entidad.configure(values=lista_estados)
        if self.var_entidad.get() not in lista_estados:
            self.var_entidad.set("Estado: Todos")

        self._recargar_municipios()
        self._recargar_colonias()
        self._recargar_calles()

    def _recargar_municipios(self):
        entidad = self.var_entidad.get()
        if entidad != "Estado: Todos":
            filas = self.controller.db.consultar(
                """
                SELECT m.nombre_municipio
                FROM municipio m
                JOIN entidad_federativa ef ON m.id_entidad_fede = ef.id_entidad_fede
                WHERE ef.nombre_entidad_fede = %s
                ORDER BY m.nombre_municipio
                """,
                (entidad,)
            )
        else:
            filas = self.controller.db.consultar(
                "SELECT nombre_municipio FROM municipio ORDER BY nombre_municipio"
            )
        lista = ["Municipio: Todos"] + [r["nombre_municipio"] for r in filas]
        self.menu_municipio.configure(values=lista)
        if self.var_municipio.get() not in lista:
            self.var_municipio.set("Municipio: Todos")

    def _recargar_colonias(self):
        municipio = self.var_municipio.get()
        entidad = self.var_entidad.get()
        if municipio != "Municipio: Todos":
            filas = self.controller.db.consultar(
                """
                SELECT DISTINCT col.nombre_colonia
                FROM colonia col
                JOIN municipio m ON col.id_municipio = m.id_municipio
                WHERE m.nombre_municipio = %s
                ORDER BY col.nombre_colonia
                """,
                (municipio,)
            )
        elif entidad != "Estado: Todos":
            filas = self.controller.db.consultar(
                """
                SELECT DISTINCT col.nombre_colonia
                FROM colonia col
                JOIN municipio m ON col.id_municipio = m.id_municipio
                JOIN entidad_federativa ef ON m.id_entidad_fede = ef.id_entidad_fede
                WHERE ef.nombre_entidad_fede = %s
                ORDER BY col.nombre_colonia
                """,
                (entidad,)
            )
        else:
            filas = self.controller.db.consultar(
                "SELECT DISTINCT nombre_colonia FROM colonia ORDER BY nombre_colonia"
            )
        lista = ["Todas las colonias"] + [r["nombre_colonia"] for r in filas]
        self.menu_colonia.configure(values=lista)
        if self.var_colonia.get() not in lista:
            self.var_colonia.set("Todas las colonias")

    def _recargar_calles(self):
        colonia = self.var_colonia.get()
        municipio = self.var_municipio.get()
        entidad = self.var_entidad.get()
        if colonia != "Todas las colonias":
            filas = self.controller.db.consultar(
                """
                SELECT DISTINCT d.calle
                FROM direccion d
                JOIN colonia col ON d.id_colonia = col.id_colonia
                WHERE col.nombre_colonia = %s AND d.direccion_recurrente_cliente = 1
                ORDER BY d.calle
                """,
                (colonia,)
            )
        elif municipio != "Municipio: Todos":
            filas = self.controller.db.consultar(
                """
                SELECT DISTINCT d.calle
                FROM direccion d
                JOIN colonia col ON d.id_colonia = col.id_colonia
                JOIN municipio m ON col.id_municipio = m.id_municipio
                WHERE m.nombre_municipio = %s AND d.direccion_recurrente_cliente = 1
                ORDER BY d.calle
                """,
                (municipio,)
            )
        elif entidad != "Estado: Todos":
            filas = self.controller.db.consultar(
                """
                SELECT DISTINCT d.calle
                FROM direccion d
                JOIN colonia col ON d.id_colonia = col.id_colonia
                JOIN municipio m ON col.id_municipio = m.id_municipio
                JOIN entidad_federativa ef ON m.id_entidad_fede = ef.id_entidad_fede
                WHERE ef.nombre_entidad_fede = %s AND d.direccion_recurrente_cliente = 1
                ORDER BY d.calle
                """,
                (entidad,)
            )
        else:
            filas = self.controller.db.consultar(
                "SELECT DISTINCT calle FROM direccion WHERE direccion_recurrente_cliente = 1 ORDER BY calle"
            )
        lista = ["Calle: Todas"] + [r["calle"] for r in filas]
        self.menu_calle.configure(values=lista)
        if self.var_calle.get() not in lista:
            self.var_calle.set("Calle: Todas")

    def _al_cambiar_entidad(self, _):
        self._recargar_municipios()
        self._recargar_colonias()
        self._recargar_calles()
        self.cargar_datos()

    def _al_cambiar_municipio(self, _):
        self._recargar_colonias()
        self._recargar_calles()
        self.cargar_datos()

    def _al_cambiar_colonia(self, _):
        self._recargar_calles()
        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self._clientes_cache.clear()

        condiciones = ["1=1"]
        params = []

        if self.controller.id_sucursal_actual:
            condiciones.append("c.id_sucursal = %s")
            params.append(self.controller.id_sucursal_actual)

        estado_sel = self.var_estado_cli.get()
        if estado_sel != "Todos":
            condiciones.append("c.estado_cliente = %s")
            params.append(estado_sel)

        historial_sel = self.var_historial.get()
        if historial_sel == "Con predicción":
            condiciones.append("p.promedio_dias_consumo IS NOT NULL")
        elif historial_sel == "Sin historial":
            condiciones.append("p.promedio_dias_consumo IS NULL")

        entidad_sel = self.var_entidad.get()
        if entidad_sel != "Estado: Todos":
            condiciones.append("ef.nombre_entidad_fede = %s")
            params.append(entidad_sel)

        municipio_sel = self.var_municipio.get()
        if municipio_sel != "Municipio: Todos":
            condiciones.append("m.nombre_municipio = %s")
            params.append(municipio_sel)

        colonia_sel = self.var_colonia.get()
        if colonia_sel != "Todas las colonias":
            condiciones.append("col.nombre_colonia = %s")
            params.append(colonia_sel)

        calle_sel = self.var_calle.get()
        if calle_sel != "Calle: Todas":
            condiciones.append("d.calle = %s")
            params.append(calle_sel)

        busqueda = self.entry_buscar.get().strip()
        if busqueda:
            condiciones.append("(c.nombre_cliente LIKE %s OR c.telefono_whatsapp_cliente LIKE %s)")
            like = f"%{busqueda}%"
            params.extend([like, like])

        where_sql = " AND ".join(condiciones)

        query = f"""
            SELECT
                c.id_cliente,
                c.nombre_cliente,
                c.telefono_whatsapp_cliente,
                c.estado_cliente,
                d.id_direccion,
                d.calle,
                d.num_exterior,
                col.nombre_colonia,
                p.promedio_dias_consumo,
                p.fecha_ultimo_ped,
                p.fecha_estimada_agotamiento
            FROM cliente c
            LEFT JOIN direccion d
                ON d.id_cliente = c.id_cliente AND d.direccion_recurrente_cliente = 1
            LEFT JOIN colonia col
                ON col.id_colonia = d.id_colonia
            LEFT JOIN municipio m
                ON m.id_municipio = col.id_municipio
            LEFT JOIN entidad_federativa ef
                ON ef.id_entidad_fede = m.id_entidad_fede
            LEFT JOIN prediccion p
                ON p.id_cliente = c.id_cliente AND p.vigente = 1
            WHERE {where_sql}
            ORDER BY c.id_cliente ASC
        """
        filas = self.controller.db.consultar(query, tuple(params))

        for f in filas:
            id_str = str(f["id_cliente"])
            self._clientes_cache[id_str] = f
            direccion_txt = armar_direccion(f["calle"], f["num_exterior"], f["nombre_colonia"])
            frec_txt = f"Cada {float(f['promedio_dias_consumo']):.0f} d" if f["promedio_dias_consumo"] else "Sin historial"
            self.tabla.insert(
                "",
                "end",
                iid=id_str,
                values=(
                    f["id_cliente"],
                    f["nombre_cliente"],
                    f["telefono_whatsapp_cliente"],
                    direccion_txt,
                    frec_txt,
                    formatear_fecha(f["fecha_ultimo_ped"]),
                    formatear_fecha(f["fecha_estimada_agotamiento"]),
                    f["estado_cliente"],
                    "✏️ Editar",
                ),
            )

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self._cargar_opciones_filtros()
        self.cargar_datos()