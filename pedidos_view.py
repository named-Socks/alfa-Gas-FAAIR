import customtkinter as ctk
from tkinter import ttk, messagebox
from database import armar_direccion


class PedidosView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.pedidos_map = {}

        # Navbar
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

        # Contenedor principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(30, 20))

        top_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(top_bar, text="Filtros rápidos:", font=("Arial", 14, "bold"), text_color="#7F8C8D").pack(side="left")

        self.combo_estado = ctk.CTkOptionMenu(
            top_bar,
            values=["Todos los estados", "REGISTRADO", "ENTREGADO", "CANCELADO", "FALLIDO"],
            width=165,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.combo_estado.pack(side="left", padx=10)

        self.combo_origen = ctk.CTkOptionMenu(
            top_bar,
            values=["Todos los orígenes", "WHATSAPP", "ADMIN"],
            width=165,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.combo_origen.pack(side="left", padx=10)

        self.entry_busqueda = ctk.CTkEntry(
            top_bar,
            placeholder_text="🔍 Buscar por cliente o folio",
            width=260,
            corner_radius=20
        )
        self.entry_busqueda.pack(side="right")
        self.entry_busqueda.bind("<KeyRelease>", lambda _: self.cargar_datos())

        # Barra de cambio de estatus
        accion_bar = ctk.CTkFrame(main_frame, fg_color="#F8F9FA", corner_radius=10)
        accion_bar.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            accion_bar,
            text="Selecciona un pedido y cambia su estatus:",
            font=("Arial", 13, "bold"),
            text_color="#2C3E50"
        ).pack(side="left", padx=15, pady=10)

        self.combo_nuevo_estado = ctk.CTkOptionMenu(
            accion_bar,
            values=["ENTREGADO", "REGISTRADO", "CANCELADO", "FALLIDO"],
            width=150,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            button_color="#D5DBDB"
        )
        self.combo_nuevo_estado.pack(side="left", padx=10)

        ctk.CTkButton(
            accion_bar,
            text="Actualizar estatus ✔",
            fg_color="#214328",
            hover_color="#18321E",
            font=("Arial", 13, "bold"),
            command=self.cambiar_estatus_pedido
        ).pack(side="left", padx=10)

        # Tabla
        columnas = ("folio", "fecha", "cliente", "dir", "litros", "monto", "origen", "estatus")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        encabezados = ["Folio", "Fecha / Hora", "Cliente", "Dirección de entrega", "Cantidad", "Monto total", "Origen", "Estatus"]
        anchos = [95, 145, 190, 290, 110, 115, 105, 115]

        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho)

        self.tabla.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    def cargar_datos(self):
        precio = self.controller.db.obtener_precio_vigente()
        self.lbl_precio.configure(
            text=f"Precio por litro: ${precio:.2f}" if precio is not None else "Precio por litro: sin definir"
        )

        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.pedidos_map.clear()

        sucursal = self.controller.id_sucursal_actual
        query = """
            SELECT
                p.id_pedido,
                p.folio,
                DATE_FORMAT(p.fecha_registro, '%%d/%%m/%%Y %%H:%%i') AS fecha_fmt,
                c.nombre_cliente,
                d.calle, d.num_exterior, d.num_interior,
                col.nombre_colonia, col.codigo_postal,
                m.nombre_municipio, ef.nombre_entidad_fede,
                COALESCE(SUM(dp.cantidad), 0) AS cantidad_total,
                MAX(pr.tipo_producto) AS tipo_producto,
                COALESCE(SUM(dp.cantidad * pp.precio_producto), 0) AS monto_total,
                p.origen_pedido,
                p.estado_pedido
            FROM pedido p
            INNER JOIN cliente c ON p.id_cliente = c.id_cliente
            INNER JOIN direccion d ON p.id_direccion_entrega = d.id_direccion
            INNER JOIN colonia col ON d.id_colonia = col.id_colonia
            INNER JOIN municipio m ON col.id_municipio = m.id_municipio
            INNER JOIN entidad_federativa ef ON m.id_entidad_fede = ef.id_entidad_fede
            INNER JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
            INNER JOIN producto pr ON dp.id_producto = pr.id_producto
            INNER JOIN precio_producto pp ON dp.id_precio = pp.id_precio
            WHERE (%s IS NULL OR p.id_sucursal = %s)
        """
        params = [sucursal, sucursal]

        estado = self.combo_estado.get()
        if estado != "Todos los estados":
            query += " AND p.estado_pedido = %s"
            params.append(estado)

        origen = self.combo_origen.get()
        if origen != "Todos los orígenes":
            query += " AND p.origen_pedido = %s"
            params.append(origen)

        texto = self.entry_busqueda.get().strip()
        if texto:
            query += " AND (c.nombre_cliente LIKE %s OR p.folio LIKE %s)"
            params += [f"%{texto}%", f"%{texto}%"]

        query += """
            GROUP BY p.id_pedido, p.folio, p.fecha_registro, c.nombre_cliente,
                     d.calle, d.num_exterior, d.num_interior, col.nombre_colonia,
                     col.codigo_postal, m.nombre_municipio, ef.nombre_entidad_fede,
                     p.origen_pedido, p.estado_pedido
            ORDER BY p.fecha_registro DESC
        """

        for fila in self.controller.db.consultar(query, params):
            unidad = "L" if fila["tipo_producto"] == "GAS_ESTACIONARIO" else "pzas"
            direccion_txt = armar_direccion(fila)
            item_id = self.tabla.insert("", "end", values=(
                fila["folio"],
                fila["fecha_fmt"],
                fila["nombre_cliente"],
                direccion_txt,
                f"{float(fila['cantidad_total']):.2f} {unidad}",
                f"${float(fila['monto_total']):,.2f}",
                fila["origen_pedido"],
                fila["estado_pedido"]
            ))
            self.pedidos_map[item_id] = fila["id_pedido"]

    def cambiar_estatus_pedido(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Primero haz clic sobre un pedido en la tabla.")
            return

        id_pedido = self.pedidos_map.get(seleccion[0])
        nuevo_estado = self.combo_nuevo_estado.get()

        if nuevo_estado == "ENTREGADO":
            sql = "UPDATE pedido SET estado_pedido = %s, fecha_entrega_real = NOW() WHERE id_pedido = %s"
        else:
            sql = "UPDATE pedido SET estado_pedido = %s WHERE id_pedido = %s"

        self.controller.db.ejecutar(sql, (nuevo_estado, id_pedido))
        self.cargar_datos()
        messagebox.showinfo("Actualizado", f"El pedido cambió a estatus: {nuevo_estado}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()