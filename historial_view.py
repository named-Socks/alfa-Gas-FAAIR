import customtkinter as ctk
from tkinter import ttk, messagebox
from database import SelectorFecha, texto_a_fecha
from PIL import Image


class HistorialView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Navbar unificado
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")

        img_icono = Image.open("/home/jayb/Documentos/GitHub/alfa-Gas-FAAIR/alfaGasIcono.png")
        self.icono_alfa = ctk.CTkImage(light_image=img_icono, dark_image=img_icono, size=(209, 71.33))

        ctk.CTkLabel(
            header,
            image=self.icono_alfa,
            text="   Historial de ventas",
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

        self.lbl_precio = ctk.CTkLabel(
            self,
            text="Precio por litro: $00.00",
            font=("Arial", 17, "bold"),
            text_color="#214328"
        )
        self.lbl_precio.pack(pady=(12, 0))

        # Contenedor principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Barra superior de filtros (letra agrandada)
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=18)

        ctk.CTkLabel(
            top_frame,
            text="Filtros rápidos:",
            font=("Arial", 17, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")

        self.combo_origen = ctk.CTkOptionMenu(
            top_frame,
            values=["Todos los orígenes", "WHATSAPP", "ADMIN"],
            width=210,
            height=44,
            font=("Arial", 16),
            dropdown_font=("Arial", 16),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.combo_origen.pack(side="left", padx=(10, 18))

        ctk.CTkLabel(
            top_frame,
            text="Desde:",
            font=("Arial", 17, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        self.entry_desde = SelectorFecha(top_frame, width=165)
        self._estilizar_selector_fecha(self.entry_desde)
        self.entry_desde.pack(side="left", padx=6)

        ctk.CTkLabel(
            top_frame,
            text="Hasta:",
            font=("Arial", 17, "bold"),
            text_color="#2C3E50"
        ).pack(side="left", padx=(8, 0))
        self.entry_hasta = SelectorFecha(top_frame, width=165)
        self._estilizar_selector_fecha(self.entry_hasta)
        self.entry_hasta.pack(side="left", padx=6)

        ctk.CTkButton(
            top_frame,
            text="🔄",
            width=46,
            height=44,
            font=("Arial", 18),
            corner_radius=8,
            fg_color="#F5CBA7",
            text_color="#000",
            command=self.limpiar_filtros
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            top_frame,
            text="🔍",
            width=46,
            height=44,
            font=("Arial", 18),
            corner_radius=8,
            fg_color="#ABEBC6",
            text_color="#000",
            command=self.cargar_datos
        ).pack(side="left", padx=4)

        self.entry_busqueda = ctk.CTkEntry(
            top_frame,
            placeholder_text="🔍 Buscar por nombre / folio",
            width=270,
            height=44,
            font=("Arial", 16),
            corner_radius=22
        )
        self.entry_busqueda.pack(side="right")
        self.entry_busqueda.bind("<KeyRelease>", lambda _: self.cargar_datos())

        # Tabla (tamaño de letra sin cambios)
        columnas = ("folio", "fecha", "nombre", "litros", "origen", "monto")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        encabezados = ["Folio", "Fecha entrega", "Cliente", "Cantidad surtida", "Origen", "Monto total"]
        anchos = [110, 170, 260, 160, 130, 140]

        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho)

        self.tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _estilizar_selector_fecha(self, selector):
        selector.configure(height=44)
        selector.btn_fecha.configure(font=("Arial", 15))
        selector.btn_limpiar.configure(width=26, height=26, font=("Arial", 13, "bold"))
        original_set_fecha = selector.set_fecha

        def set_fecha_grande(nueva_fecha):
            original_set_fecha(nueva_fecha)
            selector.btn_fecha.configure(
                font=("Arial", 15, "bold" if nueva_fecha else "normal")
            )

        selector.set_fecha = set_fecha_grande

    def limpiar_filtros(self):
        self.combo_origen.set("Todos los orígenes")
        self.entry_desde.limpiar()
        self.entry_hasta.limpiar()
        self.entry_busqueda.delete(0, "end")
        self.cargar_datos()

    def cargar_datos(self):
        try:
            desde = texto_a_fecha(self.entry_desde.get())
            hasta = texto_a_fecha(self.entry_hasta.get())
        except ValueError:
            messagebox.showwarning("Fecha inválida", "Usa el formato dd/mm/aaaa.")
            return

        precio = self.controller.db.obtener_precio_vigente()
        self.lbl_precio.configure(
            text=f"Precio por litro: ${precio:.2f}" if precio is not None else "Precio por litro: sin definir"
        )

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        sucursal = self.controller.id_sucursal_actual
        query = """
            SELECT
                p.folio,
                DATE_FORMAT(COALESCE(p.fecha_entrega_real, p.fecha_registro), '%d/%m/%Y %H:%i') AS fecha_fmt,
                c.nombre_cliente,
                COALESCE(SUM(dp.cantidad_litros), 0) AS total_cantidad,
                MAX(pr.tipo_producto) AS tipo_producto,
                p.origen_pedido,
                COALESCE(SUM(COALESCE(dp.subtotal, dp.cantidad_litros * COALESCE(dp.precio_unitario, pp.precio_producto))), 0) AS total_calculado
            FROM pedido p
            INNER JOIN cliente c ON p.id_cliente = c.id_cliente
            INNER JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
            INNER JOIN producto pr ON dp.id_producto = pr.id_producto
            LEFT JOIN precio_producto pp ON dp.id_precio = pp.id_precio
            WHERE p.estado_pedido = 'ENTREGADO'
              AND (%s IS NULL OR p.id_sucursal = %s)
        """
        params = [sucursal, sucursal]

        origen = self.combo_origen.get()
        if origen != "Todos los orígenes":
            query += " AND p.origen_pedido = %s"
            params.append(origen)

        if desde:
            query += " AND DATE(COALESCE(p.fecha_entrega_real, p.fecha_registro)) >= %s"
            params.append(desde)
        if hasta:
            query += " AND DATE(COALESCE(p.fecha_entrega_real, p.fecha_registro)) <= %s"
            params.append(hasta)

        texto = self.entry_busqueda.get().strip()
        if texto:
            query += " AND (c.nombre_cliente LIKE %s OR p.folio LIKE %s)"
            params += [f"%{texto}%", f"%{texto}%"]

        query += """
            GROUP BY p.id_pedido, p.folio, p.fecha_entrega_real, p.fecha_registro, c.nombre_cliente, p.origen_pedido
            ORDER BY COALESCE(p.fecha_entrega_real, p.fecha_registro) DESC
        """

        for fila in self.controller.db.consultar(query, params):
            unidad = "L" if fila["tipo_producto"] == "GAS_ESTACIONARIO" else "pzas"
            self.tabla.insert("", "end", values=(
                fila["folio"],
                fila["fecha_fmt"],
                fila["nombre_cliente"],
                f"{float(fila['total_cantidad']):.2f} {unidad}",
                fila["origen_pedido"],
                f"${float(fila['total_calculado']):,.2f}"
            ))

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()