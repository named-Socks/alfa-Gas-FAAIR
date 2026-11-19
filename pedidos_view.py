import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, armar_direccion


class PedidosView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # --- ENCABEZADO SUPERIOR ---
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Pedidos",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=30, pady=20)

        ctk.CTkButton(
            header,
            text="Regresar a inicio 🏠",
            fg_color="#F8F9FA",
            text_color="#214328",
            hover_color="#E2E6EA",
            font=("Arial", 14, "bold"),
            corner_radius=20,
            command=lambda: self.controller.mostrar_pantalla("menu")
        ).pack(side="right", padx=30)

        self.lbl_admin = ctk.CTkLabel(header, text="", font=("Arial", 14), text_color="#FFFFFF")
        self.lbl_admin.pack(side="right", padx=10)

        self.lbl_precio = ctk.CTkLabel(
            self,
            text="Precio por litro: $00.00",
            font=("Arial", 14, "bold"),
            text_color="#7F8C8D"
        )
        self.lbl_precio.place(relx=0.5, rely=0.07, anchor="center")

        # --- CONTENEDOR PRINCIPAL ---
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(30, 20))

        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(15, 0))
        self.entry_busqueda = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar por folio o nombre",
            width=300,
            corner_radius=20
        )
        self.entry_busqueda.pack(side="right")
        self.entry_busqueda.bind("<KeyRelease>", lambda event: self.cargar_datos())

        ctk.CTkLabel(
            main_frame,
            text="Filtros rápidos",
            font=("Arial", 14, "bold"),
            text_color="#7F8C8D"
        ).pack(anchor="w", padx=20)

        # --- FILTROS RÁPIDOS CONECTADOS A LA BD ---
        filtros_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=20, pady=10)

        estilo_combo = {
            "width": 145,
            "fg_color": "#FFFFFF",
            "text_color": "#2C3E50",
            "button_color": "#D5DBDB",
            "button_hover_color": "#BDC3C7",
            "dropdown_fg_color": "#FFFFFF",
            "dropdown_text_color": "#2C3E50"
        }

        self.combo_estado = ctk.CTkOptionMenu(
            filtros_frame, values=["Estado: Todos"],
            command=self._al_cambiar_estado, **estilo_combo
        )
        self.combo_estado.pack(side="left", padx=(0, 12))

        self.combo_ciudad = ctk.CTkOptionMenu(
            filtros_frame, values=["Ciudad: Todas"],
            command=self._al_cambiar_ciudad, **estilo_combo
        )
        self.combo_ciudad.pack(side="left", padx=(0, 12))

        self.combo_colonia = ctk.CTkOptionMenu(
            filtros_frame, values=["Colonia: Todas"],
            command=self._al_cambiar_colonia, **estilo_combo
        )
        self.combo_colonia.pack(side="left", padx=(0, 12))

        self.combo_calle = ctk.CTkOptionMenu(
            filtros_frame, values=["Calle: Todas"],
            command=lambda _: self.cargar_datos(), **estilo_combo
        )
        self.combo_calle.pack(side="left", padx=(0, 12))

        # Tu tabla pedido aún no tiene columna metodo_pago; dejamos filtro por Estatus del pedido
        self.combo_estatus = ctk.CTkOptionMenu(
            filtros_frame,
            values=["Estatus: Todos", "REGISTRADO", "ENTREGADO", "CANCELADO", "FALLIDO"],
            command=lambda _: self.cargar_datos(),
            **estilo_combo
        )
        self.combo_estatus.pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            filtros_frame,
            text="Limpiar filtros",
            width=110,
            fg_color="#E9ECEF",
            text_color="#2C3E50",
            hover_color="#D5DBDB",
            command=self.limpiar_filtros
        ).pack(side="left", padx=(5, 0))

        # --- ESTILO DEL TREEVIEW (ENCABEZADOS DE 2 RENGLONES SIN CORTARSE) ---
        style = ttk.Style()
        style.configure(
            "Pedidos.Treeview.Heading",
            background="#214328",
            foreground="#FFFFFF",
            font=("Arial", 10, "bold"),
            padding=(6, 12)  # Aumenta el alto del encabezado para 2 líneas
        )
        style.map("Pedidos.Treeview.Heading", background=[("active", "#2E5E38")])
        style.configure("Pedidos.Treeview", rowheight=32, font=("Arial", 10))

        columnas = ("id", "fecha", "cliente", "dir", "litros", "monto", "origen", "estatus", "cambiar")
        self.tabla = ttk.Treeview(
            main_frame,
            columns=columnas,
            show="headings",
            style="Pedidos.Treeview"
        )

        encabezados = [
            "Folio",
            "Fecha /\nHora",
            "Cliente",
            "Dirección de\nentrega",
            "Litros\nsolicitados",
            "Monto\ntotal",
            "Origen\npedido",
            "Estatus",
            "Cambiar\nestatus"
        ]
        anchos = [95, 115, 165, 230, 95, 95, 95, 110, 100]

        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho, minwidth=75)

        self.tabla.pack(fill="both", expand=True, padx=20, pady=20)

        # Clic en la columna "Cambiar estatus" o doble clic en la fila abre el selector
        self.tabla.bind("<ButtonRelease-1>", self._clic_en_tabla)
        self.tabla.bind("<Double-1>", self._doble_clic_fila)

    # ------------------------------------------------------------------
    # CARGA DINÁMICA DE CATÁLOGOS PARA LOS FILTROS
    # ------------------------------------------------------------------
    def cargar_opciones_filtros(self):
        # 1. Estados (entidad_federativa)
        estados = self.controller.db.consultar(
            "SELECT nombre_entidad_fede FROM entidad_federativa ORDER BY nombre_entidad_fede"
        )
        lista_estados = ["Estado: Todos"] + [r["nombre_entidad_fede"] for r in estados]
        self.combo_estado.configure(values=lista_estados)
        if self.combo_estado.get() not in lista_estados:
            self.combo_estado.set("Estado: Todos")

        self._cargar_ciudades()
        self._cargar_colonias()
        self._cargar_calles()

    def _cargar_ciudades(self):
        estado_sel = self.combo_estado.get()
        if estado_sel != "Estado: Todos":
            filas = self.controller.db.consultar("""
                SELECT m.nombre_municipio
                FROM municipio m
                JOIN entidad_federativa e ON e.id_entidad_fede = m.id_entidad_fede
                WHERE e.nombre_entidad_fede = %s
                ORDER BY m.nombre_municipio
            """, [estado_sel])
        else:
            filas = self.controller.db.consultar(
                "SELECT nombre_municipio FROM municipio ORDER BY nombre_municipio"
            )
        lista = ["Ciudad: Todas"] + [r["nombre_municipio"] for r in filas]
        self.combo_ciudad.configure(values=lista)
        if self.combo_ciudad.get() not in lista:
            self.combo_ciudad.set("Ciudad: Todas")

    def _cargar_colonias(self):
        ciudad_sel = self.combo_ciudad.get()
        estado_sel = self.combo_estado.get()

        query = """
            SELECT col.nombre_colonia
            FROM colonia col
            JOIN municipio m ON m.id_municipio = col.id_municipio
            JOIN entidad_federativa e ON e.id_entidad_fede = m.id_entidad_fede
            WHERE 1=1
        """
        params = []
        if estado_sel != "Estado: Todos":
            query += " AND e.nombre_entidad_fede = %s"
            params.append(estado_sel)
        if ciudad_sel != "Ciudad: Todas":
            query += " AND m.nombre_municipio = %s"
            params.append(ciudad_sel)
        query += " ORDER BY col.nombre_colonia"

        filas = self.controller.db.consultar(query, params)
        lista = ["Colonia: Todas"] + [r["nombre_colonia"] for r in filas]
        self.combo_colonia.configure(values=lista)
        if self.combo_colonia.get() not in lista:
            self.combo_colonia.set("Colonia: Todas")

    def _cargar_calles(self):
        colonia_sel = self.combo_colonia.get()
        ciudad_sel = self.combo_ciudad.get()

        query = """
            SELECT DISTINCT d.calle
            FROM direccion d
            JOIN colonia col ON col.id_colonia = d.id_colonia
            JOIN municipio m ON m.id_municipio = col.id_municipio
            WHERE 1=1
        """
        params = []
        if ciudad_sel != "Ciudad: Todas":
            query += " AND m.nombre_municipio = %s"
            params.append(ciudad_sel)
        if colonia_sel != "Colonia: Todas":
            query += " AND col.nombre_colonia = %s"
            params.append(colonia_sel)
        query += " ORDER BY d.calle"

        filas = self.controller.db.consultar(query, params)
        lista = ["Calle: Todas"] + [r["calle"] for r in filas]
        self.combo_calle.configure(values=lista)
        if self.combo_calle.get() not in lista:
            self.combo_calle.set("Calle: Todas")

    def _al_cambiar_estado(self, _):
        self._cargar_ciudades()
        self._cargar_colonias()
        self._cargar_calles()
        self.cargar_datos()

    def _al_cambiar_ciudad(self, _):
        self._cargar_colonias()
        self._cargar_calles()
        self.cargar_datos()

    def _al_cambiar_colonia(self, _):
        self._cargar_calles()
        self.cargar_datos()

    def limpiar_filtros(self):
        self.entry_busqueda.delete(0, "end")
        self.combo_estado.set("Estado: Todos")
        self.combo_ciudad.set("Ciudad: Todas")
        self.combo_colonia.set("Colonia: Todas")
        self.combo_calle.set("Calle: Todas")
        self.combo_estatus.set("Estatus: Todos")
        self.cargar_opciones_filtros()
        self.cargar_datos()

    # ------------------------------------------------------------------
    # CONSULTA PRINCIPAL DE PEDIDOS
    # ------------------------------------------------------------------
    def cargar_datos(self):
        precio = self.controller.db.obtener_precio_vigente()
        self.lbl_precio.configure(
            text=f"Precio por litro: ${precio:.2f}" if precio is not None else "Precio por litro: sin definir"
        )

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        sucursal = self.controller.id_sucursal_actual
        query = """
            SELECT p.id_pedido,
                   p.folio,
                   p.fecha_registro,
                   p.estado_pedido,
                   p.origen_pedido,
                   p.cantidad_litros,
                   p.total_pedido,
                   c.nombre_cliente,
                   d.calle,
                   d.num_exterior,
                   col.nombre_colonia,
                   pr.tipo_producto
            FROM pedido p
            JOIN cliente c ON c.id_cliente = p.id_cliente
            JOIN direccion d ON d.id_direccion = p.id_direccion_entrega
            JOIN colonia col ON col.id_colonia = d.id_colonia
            JOIN municipio m ON m.id_municipio = col.id_municipio
            JOIN entidad_federativa e ON e.id_entidad_fede = m.id_entidad_fede
            JOIN producto pr ON pr.id_producto = p.id_producto
            WHERE (%s IS NULL OR p.id_sucursal = %s)
        """
        params = [sucursal, sucursal]

        # Filtro de búsqueda por folio o cliente
        texto = self.entry_busqueda.get().strip()
        if texto:
            query += " AND (c.nombre_cliente LIKE %s OR p.folio LIKE %s)"
            params += [f"%{texto}%", f"%{texto}%"]

        # Filtros rápidos
        if self.combo_estado.get() != "Estado: Todos":
            query += " AND e.nombre_entidad_fede = %s"
            params.append(self.combo_estado.get())

        if self.combo_ciudad.get() != "Ciudad: Todas":
            query += " AND m.nombre_municipio = %s"
            params.append(self.combo_ciudad.get())

        if self.combo_colonia.get() != "Colonia: Todas":
            query += " AND col.nombre_colonia = %s"
            params.append(self.combo_colonia.get())

        if self.combo_calle.get() != "Calle: Todas":
            query += " AND d.calle = %s"
            params.append(self.combo_calle.get())

        if self.combo_estatus.get() != "Estatus: Todos":
            query += " AND p.estado_pedido = %s"
            params.append(self.combo_estatus.get())

        query += " ORDER BY p.id_pedido DESC"

        for fila in self.controller.db.consultar(query, params):
            unidad = "L" if fila["tipo_producto"] == "GAS_ESTACIONARIO" else "pzas"
            self.tabla.insert(
                "",
                "end",
                iid=str(fila["id_pedido"]),
                values=(
                    fila["folio"],
                    formatear_fecha(fila["fecha_registro"], "%d/%m/%y\n%H:%M"),
                    fila["nombre_cliente"],
                    armar_direccion(fila["calle"], fila["num_exterior"], fila["nombre_colonia"]),
                    f"{fila['cantidad_litros']} {unidad}",
                    f"${fila['total_pedido']}",
                    fila["origen_pedido"],
                    fila["estado_pedido"],
                    "✏ Cambiar"
                )
            )

    # ------------------------------------------------------------------
    # CAMBIAR ESTATUS DEL PEDIDO
    # ------------------------------------------------------------------
    def _clic_en_tabla(self, event):
        region = self.tabla.identify("region", event.x, event.y)
        if region != "cell":
            return
        columna = self.tabla.identify_column(event.x)
        # #9 corresponde a la 9a columna ("cambiar")
        if columna == "#9":
            item_id = self.tabla.identify_row(event.y)
            if item_id:
                self._abrir_modal_estatus(item_id)

    def _doble_clic_fila(self, event):
        item_id = self.tabla.identify_row(event.y)
        if item_id:
            self._abrir_modal_estatus(item_id)

    def _abrir_modal_estatus(self, id_pedido):
        valores = self.tabla.item(id_pedido, "values")
        folio = valores[0]
        estatus_actual = valores[7]

        modal = ctk.CTkToplevel(self)
        modal.title("Cambiar estatus")
        modal.geometry("340x210")
        modal.resizable(False, False)
        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text=f"Pedido: {folio}",
            font=("Arial", 16, "bold"),
            text_color="#214328"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            modal,
            text="Selecciona el nuevo estatus:",
            font=("Arial", 13),
            text_color="#2C3E50"
        ).pack(pady=(0, 10))

        opciones_estatus = ["REGISTRADO", "ENTREGADO", "CANCELADO", "FALLIDO"]
        combo_nuevo = ctk.CTkOptionMenu(
            modal,
            values=opciones_estatus,
            width=200,
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#214328"
        )
        combo_nuevo.set(estatus_actual)
        combo_nuevo.pack(pady=5)

        def guardar():
            nuevo_estado = combo_nuevo.get()
            if nuevo_estado == "ENTREGADO":
                sql = """
                    UPDATE pedido
                    SET estado_pedido = %s, fecha_entrega_real = NOW()
                    WHERE id_pedido = %s
                """
            else:
                sql = """
                    UPDATE pedido
                    SET estado_pedido = %s
                    WHERE id_pedido = %s
                """
            # Usa el método de escritura de tu clase Database (ejecutar / actualizar)
            if hasattr(self.controller.db, "ejecutar"):
                self.controller.db.ejecutar(sql, [nuevo_estado, id_pedido])
            else:
                self.controller.db.consultar(sql, [nuevo_estado, id_pedido])

            modal.destroy()
            self.cargar_datos()

        ctk.CTkButton(
            modal,
            text="Guardar cambio",
            fg_color="#214328",
            hover_color="#2E5E38",
            font=("Arial", 13, "bold"),
            command=guardar
        ).pack(pady=20)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_opciones_filtros()
        self.cargar_datos()