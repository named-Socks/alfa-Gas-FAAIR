import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, texto_a_fecha


class HistorialView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Barra superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Historial de ventas",
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
            text="Precio vigente por litro: $00.00",
            font=("Arial", 14, "bold"),
            text_color="#214328"
        )
        self.lbl_precio.pack(pady=(10, 0))

        # Contenedor principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Filtros y búsqueda
        filtros = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(filtros, text="Origen:", font=("Arial", 13, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 6))
        self.var_origen = ctk.StringVar(value="Todos")
        ctk.CTkOptionMenu(
            filtros,
            variable=self.var_origen,
            values=["Todos", "WHATSAPP", "ADMIN"],
            width=130,
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        ).pack(side="left", padx=(0, 15))

        ctk.CTkLabel(filtros, text="Desde:", font=("Arial", 13, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 5))
        self.entry_desde = ctk.CTkEntry(filtros, placeholder_text="dd/mm/aaaa", width=110)
        self.entry_desde.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(filtros, text="Hasta:", font=("Arial", 13, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 5))
        self.entry_hasta = ctk.CTkEntry(filtros, placeholder_text="dd/mm/aaaa", width=110)
        self.entry_hasta.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            filtros,
            text="Filtrar",
            width=80,
            fg_color="#214328",
            hover_color="#18321E",
            font=("Arial", 13, "bold"),
            command=self.cargar_datos
        ).pack(side="left")

        self.entry_buscar = ctk.CTkEntry(
            filtros,
            placeholder_text="🔍 Buscar nombre o folio...",
            width=220,
            corner_radius=20
        )
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda _: self.cargar_datos())

        # Tabla
        columnas = ("folio", "fecha", "cliente", "litros", "origen", "monto")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        encabezados = ["Folio venta", "Fecha entrega", "Cliente", "Cantidad surtida", "Origen", "Monto total"]
        anchos = [110, 150, 240, 140, 120, 140]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho)
        self.tabla.pack(fill="both", expand=True, padx=20, pady=15)

    def cargar_datos(self):
        precio_vigente = self.controller.db.obtener_precio_vigente()
        val_precio = f"{float(precio_vigente):.2f}" if precio_vigente is not None else "00.00"
        self.lbl_precio.configure(text=f"Precio vigente por litro: ${val_precio}")

        try:
            fecha_desde = texto_a_fecha(self.entry_desde.get())
            fecha_hasta = texto_a_fecha(self.entry_hasta.get())
        except ValueError:
            messagebox.showwarning("Fecha inválida", "Usa el formato dd/mm/aaaa en los filtros de fecha.")
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