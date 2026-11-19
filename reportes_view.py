import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, texto_a_fecha


class ReportesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Encabezado principal
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Reportes de ventas por zona",
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

        # Contenedor blanco principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Barra superior: título de filtros + precio vigente
        top_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            top_bar,
            text="Filtros rápidos",
            font=("Arial", 14, "bold"),
            text_color="#7F8C8D"
        ).pack(side="left")

        self.lbl_precio = ctk.CTkLabel(
            top_bar,
            text="Precio por litro: $0.00",
            font=("Arial", 14, "bold"),
            text_color="#214328"
        )
        self.lbl_precio.pack(side="right")

        # Filtros desplegables conectados a MySQL
        filtros_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=20)

        estilo_combo = {
            "width": 165,
            "fg_color": "#F8F9FA",
            "text_color": "#2C3E50",
            "button_color": "#D5DBDB",
            "button_hover_color": "#BFC9CA"
        }

        self.combo_estado = ctk.CTkOptionMenu(
            filtros_frame, values=["Estado: Todos"], command=self._al_cambiar_estado, **estilo_combo
        )
        self.combo_estado.pack(side="left", padx=(0, 12))

        self.combo_ciudad = ctk.CTkOptionMenu(
            filtros_frame, values=["Ciudad: Todas"], command=self._al_cambiar_ciudad, **estilo_combo
        )
        self.combo_ciudad.pack(side="left", padx=(0, 12))

        self.combo_colonia = ctk.CTkOptionMenu(
            filtros_frame, values=["Colonia: Todas"], command=self._al_cambiar_colonia, **estilo_combo
        )
        self.combo_colonia.pack(side="left", padx=(0, 12))

        self.combo_calle = ctk.CTkOptionMenu(
            filtros_frame, values=["Calle: Todas"], command=lambda _: self.cargar_datos(), **estilo_combo
        )
        self.combo_calle.pack(side="left", padx=(0, 12))

        self.combo_pago = ctk.CTkOptionMenu(
            filtros_frame,
            values=["Pago: Todos", "EFECTIVO", "TARJETA"],
            command=lambda _: self.cargar_datos(),
            **estilo_combo
        )
        self.combo_pago.pack(side="left")

        # Sección media: Resumen general + Filtro por fechas
        mid_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        mid_frame.pack(fill="x", padx=20, pady=20)

        resumen_frame = ctk.CTkFrame(mid_frame, fg_color="transparent")
        resumen_frame.pack(side="left")
        ctk.CTkLabel(
            resumen_frame,
            text="Resumen general de la zona seleccionada",
            font=("Arial", 12, "bold"),
            text_color="#7F8C8D"
        ).pack(anchor="w", pady=(0, 5))

        self.tabla_resumen = ttk.Treeview(
            resumen_frame, columns=("ingresos", "litros", "pedidos"), show="headings", height=1
        )
        self.tabla_resumen.heading("ingresos", text="Total de Ingresos")
        self.tabla_resumen.heading("litros", text="Total de litros vendidos")
        self.tabla_resumen.heading("pedidos", text="Total de pedidos")
        self.tabla_resumen.column("ingresos", width=160, anchor="center")
        self.tabla_resumen.column("litros", width=170, anchor="center")
        self.tabla_resumen.column("pedidos", width=140, anchor="center")
        self.tabla_resumen.pack()

        fecha_frame = ctk.CTkFrame(mid_frame, fg_color="transparent")
        fecha_frame.pack(side="right", anchor="s")
        ctk.CTkLabel(
            fecha_frame, text="Filtro por fecha", font=("Arial", 12, "bold"), text_color="#7F8C8D"
        ).pack(anchor="w")

        cont_fechas = ctk.CTkFrame(fecha_frame, fg_color="transparent")
        cont_fechas.pack()
        ctk.CTkLabel(cont_fechas, text="Desde", font=("Arial", 12, "bold"), text_color="#7F8C8D").pack(side="left", padx=5)
        self.entry_desde = ctk.CTkEntry(cont_fechas, placeholder_text="dd/mm/aaaa", width=105)
        self.entry_desde.pack(side="left")

        ctk.CTkLabel(cont_fechas, text="Hasta", font=("Arial", 12, "bold"), text_color="#7F8C8D").pack(side="left", padx=5)
        self.entry_hasta = ctk.CTkEntry(cont_fechas, placeholder_text="dd/mm/aaaa", width=105)
        self.entry_hasta.pack(side="left")

        ctk.CTkButton(
            cont_fechas, text="🔄", width=35, fg_color="#F5CBA7", text_color="#000", command=self.limpiar_filtros
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            cont_fechas, text="🔍", width=35, fg_color="#ABEBC6", text_color="#000", command=self.cargar_datos
        ).pack(side="left")

        # Tabla principal desglosada por zona
        columnas = ("ubicacion", "colonia", "fecha", "pedidos", "litros", "total")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        encabezados = [
            ("ubicacion", "Ubicación", 160),
            ("colonia", "Colonia", 190),
            ("fecha", "Última venta", 150),
            ("pedidos", "Pedidos", 95),
            ("litros", "Litros", 115),
            ("total", "Total Ingresos", 140),
        ]
        for col, texto, ancho in encabezados:
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, minwidth=80, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # ------------------------------------------------------------------
    # Carga dinámica de filtros desde MySQL
    # ------------------------------------------------------------------
    def _cargar_opciones_filtros(self):
        estados = self.controller.db.consultar(
            "SELECT nombre_entidad_fede FROM entidad_federativa ORDER BY nombre_entidad_fede"
        )
        lista_estados = ["Estado: Todos"] + [r["nombre_entidad_fede"] for r in estados]
        self.combo_estado.configure(values=lista_estados)
        if self.combo_estado.get() not in lista_estados:
            self.combo_estado.set("Estado: Todos")

        self._recargar_ciudades()
        self._recargar_colonias()
        self._recargar_calles()

    def _recargar_ciudades(self):
        estado = self.combo_estado.get()
        if estado != "Estado: Todos":
            filas = self.controller.db.consultar(
                """
                SELECT m.nombre_municipio
                FROM municipio m
                JOIN entidad_federativa ef ON m.id_entidad_fede = ef.id_entidad_fede
                WHERE ef.nombre_entidad_fede = %s
                ORDER BY m.nombre_municipio
                """,
                (estado,)
            )
        else:
            filas = self.controller.db.consultar(
                "SELECT nombre_municipio FROM municipio ORDER BY nombre_municipio"
            )
        lista = ["Ciudad: Todas"] + [r["nombre_municipio"] for r in filas]
        self.combo_ciudad.configure(values=lista)
        if self.combo_ciudad.get() not in lista:
            self.combo_ciudad.set("Ciudad: Todas")

    def _recargar_colonias(self):
        ciudad = self.combo_ciudad.get()
        if ciudad != "Ciudad: Todas":
            filas = self.controller.db.consultar(
                """
                SELECT col.nombre_colonia
                FROM colonia col
                JOIN municipio m ON col.id_municipio = m.id_municipio
                WHERE m.nombre_municipio = %s
                ORDER BY col.nombre_colonia
                """,
                (ciudad,)
            )
        else:
            filas = self.controller.db.consultar(
                "SELECT nombre_colonia FROM colonia ORDER BY nombre_colonia"
            )
        lista = ["Colonia: Todas"] + [r["nombre_colonia"] for r in filas]
        self.combo_colonia.configure(values=lista)
        if self.combo_colonia.get() not in lista:
            self.combo_colonia.set("Colonia: Todas")

    def _recargar_calles(self):
        colonia = self.combo_colonia.get()
        if colonia != "Colonia: Todas":
            filas = self.controller.db.consultar(
                """
                SELECT DISTINCT d.calle
                FROM direccion d
                JOIN colonia col ON d.id_colonia = col.id_colonia
                WHERE col.nombre_colonia = %s
                ORDER BY d.calle
                """,
                (colonia,)
            )
        else:
            filas = self.controller.db.consultar(
                "SELECT DISTINCT calle FROM direccion ORDER BY calle"
            )
        lista = ["Calle: Todas"] + [r["calle"] for r in filas]
        self.combo_calle.configure(values=lista)
        if self.combo_calle.get() not in lista:
            self.combo_calle.set("Calle: Todas")

    def _al_cambiar_estado(self, _):
        self._recargar_ciudades()
        self._recargar_colonias()
        self._recargar_calles()
        self.cargar_datos()

    def _al_cambiar_ciudad(self, _):
        self._recargar_colonias()
        self._recargar_calles()
        self.cargar_datos()

    def _al_cambiar_colonia(self, _):
        self._recargar_calles()
        self.cargar_datos()

    def limpiar_filtros(self):
        self.combo_estado.set("Estado: Todos")
        self._recargar_ciudades()
        self._recargar_colonias()
        self._recargar_calles()
        self.combo_pago.set("Pago: Todos")
        self.entry_desde.delete(0, "end")
        self.entry_hasta.delete(0, "end")
        self.cargar_datos()

    # ------------------------------------------------------------------
    # Consulta principal de ventas agrupadas por zona
    # ------------------------------------------------------------------
    def cargar_datos(self):
        try:
            desde = texto_a_fecha(self.entry_desde.get())
            hasta = texto_a_fecha(self.entry_hasta.get())
        except ValueError:
            messagebox.showwarning("Fecha inválida", "Escribe las fechas como dd/mm/aaaa, por ejemplo 19/11/2026.")
            return

        precio = self.controller.db.obtener_precio_vigente()
        self.lbl_precio.configure(
            text=f"Precio por litro: ${float(precio):.2f}" if precio is not None else "Precio por litro: sin definir"
        )

        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for item in self.tabla_resumen.get_children():
            self.tabla_resumen.delete(item)

        sucursal = self.controller.id_sucursal_actual
        query = """
            SELECT
                m.nombre_municipio AS municipio,
                col.nombre_colonia AS colonia,
                COUNT(DISTINCT p.id_pedido) AS pedidos,
                SUM(CASE WHEN prod.tipo_producto = 'GAS_ESTACIONARIO' THEN p.cantidad_litros ELSE 0 END) AS litros,
                SUM(p.total_pedido) AS total,
                MAX(COALESCE(p.fecha_entrega_real, p.fecha_registro)) AS ultima_venta
            FROM pedido p
            INNER JOIN direccion d ON p.id_direccion_entrega = d.id_direccion
            INNER JOIN colonia col ON d.id_colonia = col.id_colonia
            INNER JOIN municipio m ON col.id_municipio = m.id_municipio
            INNER JOIN entidad_federativa ef ON m.id_entidad_fede = ef.id_entidad_fede
            INNER JOIN producto prod ON p.id_producto = prod.id_producto
            WHERE p.estado_pedido = 'ENTREGADO'
              AND (%s IS NULL OR p.id_sucursal = %s)
        """
        params = [sucursal, sucursal]

        estado = self.combo_estado.get()
        if estado != "Estado: Todos":
            query += " AND ef.nombre_entidad_fede = %s"
            params.append(estado)

        ciudad = self.combo_ciudad.get()
        if ciudad != "Ciudad: Todas":
            query += " AND m.nombre_municipio = %s"
            params.append(ciudad)

        colonia = self.combo_colonia.get()
        if colonia != "Colonia: Todas":
            query += " AND col.nombre_colonia = %s"
            params.append(colonia)

        calle = self.combo_calle.get()
        if calle != "Calle: Todas":
            query += " AND d.calle = %s"
            params.append(calle)

        pago = self.combo_pago.get()
        if pago != "Pago: Todos":
            query += " AND p.metodo_pago = %s"
            params.append(pago)

        if desde:
            query += " AND DATE(COALESCE(p.fecha_entrega_real, p.fecha_registro)) >= %s"
            params.append(desde)
        if hasta:
            query += " AND DATE(COALESCE(p.fecha_entrega_real, p.fecha_registro)) <= %s"
            params.append(hasta)

        query += " GROUP BY m.nombre_municipio, col.nombre_colonia ORDER BY total DESC"

        total_ingresos = 0.0
        total_litros = 0.0
        total_pedidos = 0

        for fila in self.controller.db.consultar(query, params):
            ingresos_fila = float(fila["total"] or 0)
            litros_fila = float(fila["litros"] or 0)
            pedidos_fila = int(fila["pedidos"] or 0)

            self.tabla.insert("", "end", values=(
                fila["municipio"],
                fila["colonia"],
                formatear_fecha(fila["ultima_venta"]),
                pedidos_fila,
                f"{litros_fila:.2f} L",
                f"${ingresos_fila:,.2f}"
            ))

            total_ingresos += ingresos_fila
            total_litros += litros_fila
            total_pedidos += pedidos_fila

        self.tabla_resumen.insert(
            "",
            "end",
            values=(f"${total_ingresos:,.2f}", f"{total_litros:.2f} L", total_pedidos)
        )

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self._cargar_opciones_filtros()
        self.cargar_datos()