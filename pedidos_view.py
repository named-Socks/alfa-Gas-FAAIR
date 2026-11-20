import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, armar_direccion


class PedidosView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Barra superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Pedidos",
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

        # Contenedor blanco principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Barra superior de búsqueda y acciones
        top_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(18, 8))

        ctk.CTkLabel(top_bar, text="Filtros:", font=("Arial", 15, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 10))

        self.var_estado = ctk.StringVar(value="Todos")
        ctk.CTkOptionMenu(
            top_bar,
            variable=self.var_estado,
            values=["Todos", "REGISTRADO", "ENTREGADO", "CANCELADO", "FALLIDO"],
            width=165,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        ).pack(side="left", padx=(0, 12))

        self.var_origen = ctk.StringVar(value="Todos los orígenes")
        ctk.CTkOptionMenu(
            top_bar,
            variable=self.var_origen,
            values=["Todos los orígenes", "WHATSAPP", "ADMIN"],
            width=195,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        ).pack(side="left", padx=(0, 12))

        self.entry_buscar = ctk.CTkEntry(
            top_bar,
            placeholder_text="🔍 Buscar por folio o cliente...",
            width=290,
            height=38,
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda _: self.cargar_datos())

        # Barra de cambio de estatus
        accion_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        accion_bar.pack(fill="x", padx=20, pady=(6, 8))

        ctk.CTkLabel(
            accion_bar,
            text="Cambiar estatus del pedido seleccionado a:",
            font=("Arial", 15, "bold"),
            text_color="#2C3E50"
        ).pack(side="left", padx=(0, 10))

        self.var_nuevo_estatus = ctk.StringVar(value="ENTREGADO")
        ctk.CTkOptionMenu(
            accion_bar,
            variable=self.var_nuevo_estatus,
            values=["REGISTRADO", "ENTREGADO", "CANCELADO", "FALLIDO"],
            width=165,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB"
        ).pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            accion_bar,
            text="Actualizar estatus",
            fg_color="#214328",
            hover_color="#18321E",
            text_color="#FFFFFF",
            font=("Arial", 15, "bold"),
            height=38,
            corner_radius=8,
            command=self.cambiar_estatus_pedido
        ).pack(side="left")

        # Contenedor de tabla con barras de desplazamiento
        tabla_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=15)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal")

        columnas = ("folio", "fecha", "cliente", "direccion", "cantidad", "monto", "origen", "estatus")
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
            "Folio", "Fecha registro", "Cliente", "Dirección de entrega",
            "Cantidad", "Monto Total", "Origen", "Estado"
        ]
        anchos = [115, 175, 210, 280, 125, 140, 130, 140]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho, minwidth=ancho)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)

    def cargar_datos(self):
        precio_vigente = self.controller.db.obtener_precio_vigente()
        val_precio = f"{float(precio_vigente):.2f}" if precio_vigente is not None else "00.00"
        self.lbl_precio.configure(text=f"Precio vigente por litro (GLP-01): ${val_precio}")

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        condiciones = ["1=1"]
        params = []

        if self.controller.id_sucursal_actual:
            condiciones.append("p.id_sucursal = %s")
            params.append(self.controller.id_sucursal_actual)

        estado_sel = self.var_estado.get()
        if estado_sel != "Todos":
            condiciones.append("p.estado_pedido = %s")
            params.append(estado_sel)

        origen_sel = self.var_origen.get()
        if origen_sel != "Todos los orígenes":
            condiciones.append("p.origen_pedido = %s")
            params.append(origen_sel)

        busqueda = self.entry_buscar.get().strip()
        if busqueda:
            condiciones.append("(p.folio LIKE %s OR c.nombre_cliente LIKE %s)")
            like = f"%{busqueda}%"
            params.extend([like, like])

        where_sql = " AND ".join(condiciones)

        query = f"""
            SELECT
                p.id_pedido,
                p.folio,
                p.fecha_registro,
                c.nombre_cliente,
                d.calle,
                d.num_exterior,
                col.nombre_colonia,
                COALESCE(SUM(dp.cantidad), 0) AS total_cantidad,
                COALESCE(SUM(dp.cantidad * pp.precio_producto), 0) AS total_monto,
                p.origen_pedido,
                p.estado_pedido
            FROM pedido p
            JOIN cliente c ON c.id_cliente = p.id_cliente
            JOIN direccion d ON d.id_direccion = p.id_direccion_entrega
            JOIN colonia col ON col.id_colonia = d.id_colonia
            LEFT JOIN detalle_pedido dp ON dp.id_pedido = p.id_pedido
            LEFT JOIN precio_producto pp ON pp.id_precio = dp.id_precio
            WHERE {where_sql}
            GROUP BY p.id_pedido, p.folio, p.fecha_registro, c.nombre_cliente,
                     d.calle, d.num_exterior, col.nombre_colonia, p.origen_pedido, p.estado_pedido
            ORDER BY p.id_pedido DESC
        """
        filas = self.controller.db.consultar(query, tuple(params))

        for f in filas:
            self.tabla.insert(
                "",
                "end",
                iid=str(f["id_pedido"]),
                values=(
                    f["folio"],
                    formatear_fecha(f["fecha_registro"], "%d/%m/%Y %H:%M"),
                    f["nombre_cliente"],
                    armar_direccion(f["calle"], f["num_exterior"], f["nombre_colonia"]),
                    f"{float(f['total_cantidad']):.2f} L",
                    f"${float(f['total_monto']):,.2f}",
                    f["origen_pedido"],
                    f["estado_pedido"],
                ),
            )

    def cambiar_estatus_pedido(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona un pedido", "Haz clic sobre un pedido en la tabla para cambiar su estatus.")
            return

        id_pedido = seleccion[0]
        nuevo_estado = self.var_nuevo_estatus.get()

        if nuevo_estado == "ENTREGADO":
            query = "UPDATE pedido SET estado_pedido = %s, fecha_entrega_real = NOW() WHERE id_pedido = %s"
        else:
            query = "UPDATE pedido SET estado_pedido = %s, fecha_entrega_real = NULL WHERE id_pedido = %s"

        self.controller.db.ejecutar(query, (nuevo_estado, id_pedido))
        self.cargar_datos()
        messagebox.showinfo("Estatus actualizado", f"El pedido quedó marcado como {nuevo_estado}.")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()