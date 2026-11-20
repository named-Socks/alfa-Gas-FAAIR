import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, texto_a_fecha, SelectorFecha


class HistorialView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Barra superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Historial de ventas",
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

        self.lbl_precio = ctk.CTkLabel(
            self,
            text="Precio vigente por litro: $00.00",
            font=("Arial", 16, "bold"),
            text_color="#214328"
        )
        self.lbl_precio.pack(pady=(12, 0))

        # Contenedor principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Filtros con calendario clicable y búsqueda
        filtros = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros.pack(fill="x", padx=20, pady=(18, 8))

        ctk.CTkLabel(filtros, text="Origen:", font=("Arial", 15, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 8))
        self.var_origen = ctk.StringVar(value="Todos")
        ctk.CTkOptionMenu(
            filtros,
            variable=self.var_origen,
            values=["Todos", "WHATSAPP", "ADMIN"],
            width=150,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        ).pack(side="left", padx=(0, 16))

        ctk.CTkLabel(filtros, text="Desde:", font=("Arial", 15, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 6))
        self.entry_desde = SelectorFecha(filtros, placeholder="Fecha inicio", width=180, on_change=self.cargar_datos)
        self.entry_desde.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(filtros, text="Hasta:", font=("Arial", 15, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 6))
        self.entry_hasta = SelectorFecha(filtros, placeholder="Fecha fin", width=180, on_change=self.cargar_datos)
        self.entry_hasta.pack(side="left", padx=(0, 12))

        self.entry_buscar = ctk.CTkEntry(
            filtros,
            placeholder_text="🔍 Buscar nombre o folio...",
            width=260,
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

        columnas = ("folio", "fecha", "cliente", "litros", "origen", "monto")
        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        encabezados = ["Folio venta", "Fecha entrega", "Cliente", "Cantidad surtida", "Origen", "Monto total"]
        anchos = [145, 185, 280, 180, 140, 165]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho, minwidth=ancho)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)

    def cargar_datos(self):
        precio_vigente = self.controller.db.obtener_precio_vigente()
        val_precio = f"{float(precio_vigente):.2f}" if precio_vigente is not None else "00.00"
        self.lbl_precio.configure(text=f"Precio vigente por litro: ${val_precio}")

        try:
            fecha_desde = texto_a_fecha(self.entry_desde.get())
            fecha_hasta = texto_a_fecha(self.entry_hasta.get())
        except ValueError:
            messagebox.showwarning("Fecha inválida", "Selecciona una fecha válida en el calendario.")
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        condiciones = ["p.estado_pedido = 'ENTREGADO'"]
        params = []

        if self.controller.id_sucursal_actual:
            condiciones.append("p.id_sucursal = %s")
            params.append(self.controller.id_sucursal_actual)

        origen_sel = self.var_origen.get()
        if origen_sel != "Todos":
            condiciones.append("p.origen_pedido = %s")
            params.append(origen_sel)

        if fecha_desde:
            condiciones.append("DATE(COALESCE(p.fecha_entrega_real, p.fecha_registro)) >= %s")
            params.append(fecha_desde)

        if fecha_hasta:
            condiciones.append("DATE(COALESCE(p.fecha_entrega_real, p.fecha_registro)) <= %s")
            params.append(fecha_hasta)

        busqueda = self.entry_buscar.get().strip()
        if busqueda:
            condiciones.append("(p.folio LIKE %s OR c.nombre_cliente LIKE %s)")
            like = f"%{busqueda}%"
            params.extend([like, like])

        where_sql = " AND ".join(condiciones)

        query = f"""
            SELECT
                p.folio,
                COALESCE(p.fecha_entrega_real, p.fecha_registro) AS fecha_venta,
                c.nombre_cliente,
                COALESCE(SUM(dp.cantidad), 0) AS total_litros,
                p.origen_pedido,
                COALESCE(SUM(dp.cantidad * pp.precio_producto), 0) AS total_monto
            FROM pedido p
            JOIN cliente c ON c.id_cliente = p.id_cliente
            JOIN detalle_pedido dp ON dp.id_pedido = p.id_pedido
            JOIN precio_producto pp ON pp.id_precio = dp.id_precio
            WHERE {where_sql}
            GROUP BY p.id_pedido, p.folio, fecha_venta, c.nombre_cliente, p.origen_pedido
            ORDER BY fecha_venta DESC
        """
        filas = self.controller.db.consultar(query, tuple(params))

        for f in filas:
            self.tabla.insert(
                "",
                "end",
                values=(
                    f["folio"],
                    formatear_fecha(f["fecha_venta"], "%d/%m/%Y %H:%M"),
                    f["nombre_cliente"],
                    f"{float(f['total_litros']):.2f} L",
                    f["origen_pedido"],
                    f"${float(f['total_monto']):,.2f}",
                ),
            )

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()