import csv
from datetime import datetime
import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from database import formatear_fecha, texto_a_fecha, SelectorFecha
from PIL import Image


class ReportesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Encabezado principal
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")

        img_icono = Image.open("/home/jayb/Documentos/GitHub/alfa-Gas-FAAIR/alfaGasIcono.png")
        self.icono_alfa = ctk.CTkImage(light_image=img_icono, dark_image=img_icono, size=(209, 71.33))

        ctk.CTkLabel(
            header,
            image=self.icono_alfa,
            text="   Reportes de ventas por zona",
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

        # Barra superior dentro de la tarjeta: título de filtros + precio vigente + exportar (letra agrandada)
        top_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(
            top_bar,
            text="Filtros rápidos",
            font=("Arial", 17, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")

        ctk.CTkButton(
            top_bar,
            text="📥 Exportar CSV",
            fg_color="#214328",
            hover_color="#18321E",
            text_color="#FFFFFF",
            font=("Arial", 16, "bold"),
            height=42,
            corner_radius=10,
            command=self.exportar_csv
        ).pack(side="right", padx=(16, 0))

        self.lbl_precio = ctk.CTkLabel(
            top_bar,
            text="Precio por litro: $0.00",
            font=("Arial", 17, "bold"),
            text_color="#214328"
        )
        self.lbl_precio.pack(side="right")

        # Filtros desplegables conectados a MySQL (letra agrandada)
        filtros_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=20)

        estilo_combo = {
            "width": 195,
            "height": 44,
            "font": ("Arial", 16),
            "dropdown_font": ("Arial", 16),
            "fg_color": "#F8F9FA",
            "text_color": "#2C3E50",
            "button_color": "#D5DBDB",
            "button_hover_color": "#BFC9CA"
        }

        self.combo_estado = ctk.CTkOptionMenu(
            filtros_frame, values=["Estado: Todos"], command=self._al_cambiar_estado, **estilo_combo
        )
        self.combo_estado.pack(side="left", padx=(0, 10))

        self.combo_ciudad = ctk.CTkOptionMenu(
            filtros_frame, values=["Ciudad: Todas"], command=self._al_cambiar_ciudad, **estilo_combo
        )
        self.combo_ciudad.pack(side="left", padx=(0, 10))

        self.combo_colonia = ctk.CTkOptionMenu(
            filtros_frame, values=["Colonia: Todas"], command=self._al_cambiar_colonia, **estilo_combo
        )
        self.combo_colonia.pack(side="left", padx=(0, 10))

        self.combo_calle = ctk.CTkOptionMenu(
            filtros_frame, values=["Calle: Todas"], command=lambda _: self.cargar_datos(), **estilo_combo
        )
        self.combo_calle.pack(side="left")

        # Sección media: Tarjetas de Resumen general + Filtro por fechas (letra agrandada)
        mid_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        mid_frame.pack(fill="x", padx=20, pady=16)

        resumen_frame = ctk.CTkFrame(mid_frame, fg_color="transparent")
        resumen_frame.pack(side="left")
        ctk.CTkLabel(
            resumen_frame,
            text="Resumen general de la zona seleccionada",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 6))

        cards_row = ctk.CTkFrame(resumen_frame, fg_color="transparent")
        cards_row.pack(anchor="w")

        self.lbl_total_ingresos = self._crear_tarjeta_resumen(cards_row, "💰 Total de Ingresos", "$0.00")
        self.lbl_total_litros = self._crear_tarjeta_resumen(cards_row, "⛽ Total de litros vendidos", "0.00 L")
        self.lbl_total_pedidos = self._crear_tarjeta_resumen(cards_row, "📦 Total de pedidos", "0", ultimo=True)

        fecha_frame = ctk.CTkFrame(mid_frame, fg_color="transparent")
        fecha_frame.pack(side="right", anchor="s")
        ctk.CTkLabel(
            fecha_frame, text="Filtro por fecha", font=("Arial", 16, "bold"), text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 6))

        cont_fechas = ctk.CTkFrame(fecha_frame, fg_color="transparent")
        cont_fechas.pack()
        ctk.CTkLabel(cont_fechas, text="Desde:", font=("Arial", 16, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 5))
        self.entry_desde = SelectorFecha(cont_fechas, placeholder="Desde", width=160, on_change=self.cargar_datos)
        self._estilizar_selector_fecha(self.entry_desde)
        self.entry_desde.pack(side="left")

        ctk.CTkLabel(cont_fechas, text="Hasta:", font=("Arial", 16, "bold"), text_color="#2C3E50").pack(side="left", padx=(8, 5))
        self.entry_hasta = SelectorFecha(cont_fechas, placeholder="Hasta", width=160, on_change=self.cargar_datos)
        self._estilizar_selector_fecha(self.entry_hasta)
        self.entry_hasta.pack(side="left")

        ctk.CTkButton(
            cont_fechas, text="🔄", width=44, height=44, font=("Arial", 18), corner_radius=8,
            fg_color="#F5CBA7", text_color="#000", command=self.limpiar_filtros
        ).pack(side="left", padx=(8, 4))
        ctk.CTkButton(
            cont_fechas, text="🔍", width=44, height=44, font=("Arial", 18), corner_radius=8,
            fg_color="#ABEBC6", text_color="#000", command=self.cargar_datos
        ).pack(side="left")

        # Tabla principal desglosada por zona (tamaño de letra sin cambios)
        tabla_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal")

        columnas = ("ubicacion", "colonia", "fecha", "pedidos", "litros", "total")
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
            ("ubicacion", "Ubicación", 180),
            ("colonia", "Colonia", 220),
            ("fecha", "Última venta", 170),
            ("pedidos", "Pedidos", 120),
            ("litros", "Litros", 145),
            ("total", "Total Ingresos", 175),
        ]
        for col, texto, ancho in encabezados:
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, minwidth=ancho, anchor="center")

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)

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

    # ------------------------------------------------------------------
    # Tarjeta individual para los indicadores totales
    # ------------------------------------------------------------------
    def _crear_tarjeta_resumen(self, parent, titulo, valor_inicial, ultimo=False):
        card = ctk.CTkFrame(
            parent,
            fg_color="#FDEDEC",
            corner_radius=12,
            border_width=1,
            border_color="#F1948A",
            width=215,
            height=88
        )
        card.pack(side="left", padx=(0, 0 if ultimo else 12))
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 15, "bold"),
            text_color="#922B21"
        ).pack(anchor="w", padx=14, pady=(10, 2))

        lbl_valor = ctk.CTkLabel(
            card,
            text=valor_inicial,
            font=("Arial", 24, "bold"),
            text_color="#C0392B"
        )
        lbl_valor.pack(anchor="w", padx=14)
        return lbl_valor

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
        self.entry_desde.limpiar()
        self.entry_hasta.limpiar()
        self.cargar_datos()

    def exportar_csv(self):
        filas = [self.tabla.item(item, "values") for item in self.tabla.get_children()]
        if not filas:
            messagebox.showinfo("Sin datos", "No hay registros en la tabla para exportar.")
            return

        nombre_sugerido = f"reporte_zonas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        ruta = filedialog.asksaveasfilename(
            title="Exportar reporte por zona",
            defaultextension=".csv",
            initialfile=nombre_sugerido,
            filetypes=[("Archivo CSV (Excel)", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return

        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["Ubicación", "Colonia", "Última venta", "Pedidos", "Litros", "Total Ingresos"])
                for fila in filas:
                    writer.writerow(fila)
            messagebox.showinfo("Exportación exitosa", f"El reporte se guardó en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al exportar", f"No se pudo guardar el archivo:\n{e}")

    # ------------------------------------------------------------------
    # Consulta principal de ventas agrupadas por zona
    # ------------------------------------------------------------------
    def cargar_datos(self):
        try:
            desde = texto_a_fecha(self.entry_desde.get())
            hasta = texto_a_fecha(self.entry_hasta.get())
        except ValueError:
            messagebox.showwarning("Fecha inválida", "Selecciona una fecha válida en el calendario.")
            return

        precio = self.controller.db.obtener_precio_vigente()
        self.lbl_precio.configure(
            text=f"Precio por litro: ${float(precio):.2f}" if precio is not None else "Precio por litro: sin definir"
        )

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        sucursal = self.controller.id_sucursal_actual
        query = """
            SELECT
                m.nombre_municipio AS municipio,
                col.nombre_colonia AS colonia,
                COUNT(DISTINCT p.id_pedido) AS pedidos,
                COALESCE(SUM(CASE WHEN prod.tipo_producto = 'GAS_ESTACIONARIO' THEN dp.cantidad_litros ELSE 0 END), 0) AS litros,
                COALESCE(SUM(COALESCE(dp.subtotal, dp.cantidad_litros * COALESCE(dp.precio_unitario, pp.precio_producto))), 0) AS total,
                MAX(COALESCE(p.fecha_entrega_real, p.fecha_registro)) AS ultima_venta
            FROM pedido p
            INNER JOIN direccion d ON p.id_direccion_entrega = d.id_direccion
            INNER JOIN colonia col ON d.id_colonia = col.id_colonia
            INNER JOIN municipio m ON col.id_municipio = m.id_municipio
            INNER JOIN entidad_federativa ef ON m.id_entidad_fede = ef.id_entidad_fede
            INNER JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
            INNER JOIN producto prod ON dp.id_producto = prod.id_producto
            LEFT JOIN precio_producto pp ON dp.id_precio = pp.id_precio
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

        self.lbl_total_ingresos.configure(text=f"${total_ingresos:,.2f}")
        self.lbl_total_litros.configure(text=f"{total_litros:.2f} L")
        self.lbl_total_pedidos.configure(text=str(total_pedidos))

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self._cargar_opciones_filtros()
        self.cargar_datos()