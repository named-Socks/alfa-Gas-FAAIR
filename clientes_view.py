import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, armar_direccion


class ModalEditarCliente(ctk.CTkToplevel):
    """Ventana emergente para editar los datos y dirección vigente de un cliente."""

    def __init__(self, parent, db, datos_cliente, colonias_map, al_guardar):
        super().__init__(parent)
        self.db = db
        self.datos_cliente = datos_cliente
        self.colonias_map = colonias_map
        self.al_guardar = al_guardar

        self.title("Editar cliente - Alfa Gas")
        self.geometry("540x670")
        self.resizable(False, False)
        self.configure(fg_color="#F4F6F7")
        self.transient(parent.winfo_toplevel())
        self.bind("<Escape>", lambda _: self.destroy())

        # Encabezado verde institucional
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=68)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text=f"✏️  Editar cliente  #{datos_cliente['id_cliente']}",
            font=("Arial", 20, "bold"),
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
            font=("Arial", 15, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", padx=24, pady=(18, 4))
        self.entry_nombre = ctk.CTkEntry(
            card,
            height=40,
            font=("Arial", 15),
            corner_radius=8,
            border_color="#BDC3C7"
        )
        self.entry_nombre.pack(fill="x", padx=24)
        self.entry_nombre.insert(0, datos_cliente.get("nombre_cliente") or "")

        # Fila: Teléfono + Estatus
        fila_tel_est = ctk.CTkFrame(card, fg_color="transparent")
        fila_tel_est.pack(fill="x", padx=24, pady=(12, 0))
        fila_tel_est.grid_columnconfigure((0, 1), weight=1, uniform="tel_est")

        col_tel = ctk.CTkFrame(fila_tel_est, fg_color="transparent")
        col_tel.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        ctk.CTkLabel(
            col_tel,
            text="Teléfono WhatsApp",
            font=("Arial", 15, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 4))
        self.entry_telefono = ctk.CTkEntry(
            col_tel,
            height=40,
            font=("Arial", 15),
            corner_radius=8,
            border_color="#BDC3C7"
        )
        self.entry_telefono.pack(fill="x")
        self.entry_telefono.insert(0, datos_cliente.get("telefono_whatsapp_cliente") or "")

        col_est = ctk.CTkFrame(fila_tel_est, fg_color="transparent")
        col_est.grid(row=0, column=1, padx=(8, 0), sticky="ew")
        ctk.CTkLabel(
            col_est,
            text="Estatus del cliente",
            font=("Arial", 15, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 4))
        estatus_actual = datos_cliente.get("estado_cliente") or "ACTIVO"
        self.var_estatus = ctk.StringVar(value=estatus_actual)
        self.menu_estatus = ctk.CTkOptionMenu(
            col_est,
            variable=self.var_estatus,
            values=["ACTIVO", "PENDIENTE_REGISTRO", "INACTIVO", "BAJA"],
            height=40,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
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
            font=("Arial", 16, "bold"),
            text_color="#214328"
        ).pack(anchor="w", padx=24, pady=(0, 8))

        # Campo: Colonia
        ctk.CTkLabel(
            card,
            text="Colonia",
            font=("Arial", 15, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", padx=24, pady=(2, 4))

        nombres_colonias = list(colonias_map.keys())
        opciones_colonia = ["Sin colonia"] + nombres_colonias if nombres_colonias else ["Sin colonia"]
        colonia_actual = datos_cliente.get("nombre_colonia")
        valor_inicial_col = colonia_actual if colonia_actual in colonias_map else "Sin colonia"

        self.var_colonia = ctk.StringVar(value=valor_inicial_col)
        self.menu_colonia = ctk.CTkOptionMenu(
            card,
            variable=self.var_colonia,
            values=opciones_colonia,
            height=40,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
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
            font=("Arial", 15, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 4))
        self.entry_calle = ctk.CTkEntry(
            col_calle,
            height=40,
            font=("Arial", 15),
            corner_radius=8,
            border_color="#BDC3C7"
        )
        self.entry_calle.pack(fill="x")
        self.entry_calle.insert(0, datos_cliente.get("calle") or "")

        col_num = ctk.CTkFrame(fila_dir, fg_color="transparent")
        col_num.grid(row=0, column=1, padx=(8, 0), sticky="ew")
        ctk.CTkLabel(
            col_num,
            text="Núm. ext.",
            font=("Arial", 15, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 4))
        self.entry_num = ctk.CTkEntry(
            col_num,
            height=40,
            font=("Arial", 15),
            corner_radius=8,
            border_color="#BDC3C7"
        )
        self.entry_num.pack(fill="x")
        self.entry_num.insert(0, str(datos_cliente.get("num_exterior") or ""))
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
            font=("Arial", 15, "bold"),
            corner_radius=8,
            command=self.destroy
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            fila_botones,
            text="Guardar cambios",
            height=44,
            fg_color="#214328",
            text_color="#FFFFFF",
            hover_color="#18321E",
            font=("Arial", 15, "bold"),
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
            self.lbl_error.configure(text=f"Error al actualizar en MySQL: {e}")
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
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Clientes y predicciones",
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

        # Barra superior de filtros y búsqueda
        top_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(18, 8))

        ctk.CTkLabel(top_bar, text="Filtros:", font=("Arial", 15, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 10))

        self.var_estado_cli = ctk.StringVar(value="Todos")
        self.menu_estado = ctk.CTkOptionMenu(
            top_bar,
            variable=self.var_estado_cli,
            values=["Todos", "ACTIVO", "PENDIENTE_REGISTRO", "INACTIVO", "BAJA"],
            width=205,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.menu_estado.pack(side="left", padx=(0, 12))

        self.var_colonia = ctk.StringVar(value="Todas las colonias")
        self.menu_colonia = ctk.CTkOptionMenu(
            top_bar,
            variable=self.var_colonia,
            values=["Todas las colonias"],
            width=220,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.menu_colonia.pack(side="left", padx=(0, 12))

        self.entry_buscar = ctk.CTkEntry(
            top_bar,
            placeholder_text="🔍 Buscar por nombre o teléfono...",
            width=310,
            height=38,
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda _: self.cargar_datos())

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
        anchos = [65, 210, 140, 280, 130, 145, 175, 155, 115]
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
            al_guardar=self.cargar_datos
        )

    def _cargar_colonias(self):
        filas = self.controller.db.consultar(
            "SELECT MIN(id_colonia) AS id_colonia, nombre_colonia FROM colonia GROUP BY nombre_colonia ORDER BY nombre_colonia"
        )
        self._colonias_map = {f["nombre_colonia"]: f["id_colonia"] for f in filas}
        opciones = ["Todas las colonias"] + list(self._colonias_map.keys())
        self.menu_colonia.configure(values=opciones)

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

        colonia_sel = self.var_colonia.get()
        if colonia_sel != "Todas las colonias":
            condiciones.append("col.nombre_colonia = %s")
            params.append(colonia_sel)

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
        self._cargar_colonias()
        self.cargar_datos()