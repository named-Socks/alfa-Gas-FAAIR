import customtkinter as ctk
from tkinter import ttk
from database import formatear_fecha, armar_direccion


class ClientesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

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

        columnas = ("id", "nombre", "telefono", "direccion", "frecuencia", "ultima", "proxima", "estatus")
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
            "Frecuencia", "Último pedido", "Próximo estimado", "Estatus"
        ]
        anchos = [65, 220, 140, 290, 135, 150, 180, 165]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho, minwidth=ancho)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)

    def _cargar_colonias(self):
        filas = self.controller.db.consultar("SELECT DISTINCT nombre_colonia FROM colonia ORDER BY nombre_colonia")
        opciones = ["Todas las colonias"] + [f["nombre_colonia"] for f in filas]
        self.menu_colonia.configure(values=opciones)

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

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
                d.calle,
                d.num_exterior,
                col.nombre_colonia,
                p.promedio_dias_consumo,
                p.fecha_ultimo_pedido,
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
            direccion_txt = armar_direccion(f["calle"], f["num_exterior"], f["nombre_colonia"])
            frec_txt = f"Cada {float(f['promedio_dias_consumo']):.0f} d" if f["promedio_dias_consumo"] else "Sin historial"
            self.tabla.insert(
                "",
                "end",
                values=(
                    f["id_cliente"],
                    f["nombre_cliente"],
                    f["telefono_whatsapp_cliente"],
                    direccion_txt,
                    frec_txt,
                    formatear_fecha(f["fecha_ultimo_pedido"]),
                    formatear_fecha(f["fecha_estimada_agotamiento"]),
                    f["estado_cliente"],
                ),
            )

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self._cargar_colonias()
        self.cargar_datos()