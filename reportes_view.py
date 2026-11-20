import csv
from datetime import datetime
import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from database import texto_a_fecha, SelectorFecha


class ReportesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._filas_reporte = []

        # Barra superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Reportes de ventas por zona",
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

        # Contenedor principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Fila 1 de filtros geográficos
        filtros_geo = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_geo.pack(fill="x", padx=20, pady=(18, 6))

        self.var_estado = ctk.StringVar(value="Todos los estados")
        self.menu_estado = ctk.CTkOptionMenu(
            filtros_geo,
            variable=self.var_estado,
            values=["Todos los estados"],
            width=195,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.menu_estado.pack(side="left", padx=(0, 12))

        self.var_municipio = ctk.StringVar(value="Todos los municipios")
        self.menu_municipio = ctk.CTkOptionMenu(
            filtros_geo,
            variable=self.var_municipio,
            values=["Todos los municipios"],
            width=210,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.menu_municipio.pack(side="left", padx=(0, 12))

        self.var_colonia = ctk.StringVar(value="Todas las colonias")
        self.menu_colonia = ctk.CTkOptionMenu(
            filtros_geo,
            variable=self.var_colonia,
            values=["Todas las colonias"],
            width=210,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.menu_colonia.pack(side="left", padx=(0, 12))

        self.entry_calle = ctk.CTkEntry(
            filtros_geo,
            placeholder_text="Filtrar por calle...",
            width=220,
            height=38,
            font=("Arial", 14)
        )
        self.entry_calle.pack(side="left")
        self.entry_calle.bind("<KeyRelease>", lambda _: self.cargar_datos())

        # Fila 2 de fechas con calendario clicable y exportación
        filtros_fecha = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_fecha.pack(fill="x", padx=20, pady=(6, 12))

        ctk.CTkLabel(filtros_fecha, text="Desde:", font=("Arial", 15, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 6))
        self.entry_desde = SelectorFecha(filtros_fecha, placeholder="Fecha inicio", width=180, on_change=self.cargar_datos)
        self.entry_desde.pack(side="left", padx=(0, 14))

        ctk.CTkLabel(filtros_fecha, text="Hasta:", font=("Arial", 15, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 6))
        self.entry_hasta = SelectorFecha(filtros_fecha, placeholder="Fecha fin", width=180, on_change=self.cargar_datos)
        self.entry_hasta.pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            filtros_fecha,
            text="📥 Exportar CSV",
            width=165,
            height=38,
            fg_color="#214328",
            hover_color="#18321E",
            font=("Arial", 15, "bold"),
            command=self.exportar_csv
        ).pack(side="right")

        # Tarjetas de resumen ejecutivo
        tarjetas = ctk.CTkFrame(main_frame, fg_color="transparent")
        tarjetas.pack(fill="x", padx=20, pady=8)
        tarjetas.grid_columnconfigure((0, 1, 2), weight=1)

        self.lbl_total_ingresos = self._crear_kpi(tarjetas, 0, "Total de Ingresos", "$0.00")
        self.lbl_total_litros = self._crear_kpi(tarjetas, 1, "Total de litros vendidos", "0.00 L")
        self.lbl_total_pedidos = self._crear_kpi(tarjetas, 2, "Total de pedidos", "0")

        # Contenedor de tabla con barras de desplazamiento
        tabla_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=15)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal")

        columnas = ("ubicacion", "colonia", "calle", "pedidos", "litros", "ingresos")
        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        encabezados = ["Estado / Municipio", "Colonia", "Calle", "Pedidos", "Litros vendidos", "Total Ingresos"]
        anchos = [240, 200, 240, 120, 175, 175]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho, minwidth=ancho)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)

    def _crear_kpi(self, parent, col, titulo, valor_inicial):
        box = ctk.CTkFrame(parent, fg_color="#F8F9FA", corner_radius=12, border_width=1, border_color="#D5DBDB")
        box.grid(row=0, column=col, padx=8, sticky="ew")
        ctk.CTkLabel(box, text=titulo, font=("Arial", 15, "bold"), text_color="#7F8C8D").pack(pady=(12, 4))
        lbl = ctk.CTkLabel(box, text=valor_inicial, font=("Arial", 24, "bold"), text_color="#214328")
        lbl.pack(pady=(0, 12))
        return lbl

    def _cargar_catalogos(self):
        estados = self.controller.db.consultar("SELECT DISTINCT nombre_entidad_fede FROM entidad_federativa ORDER BY nombre_entidad_fede")
        self.menu_estado.configure(values=["Todos los estados"] + [e["nombre_entidad_fede"] for e in estados])

        municipios = self.controller.db.consultar("SELECT DISTINCT nombre_municipio FROM municipio ORDER BY nombre_municipio")
        self.menu_municipio.configure(values=["Todos los municipios"] + [m["nombre_municipio"] for m in municipios])

        colonias = self.controller.db.consultar("SELECT DISTINCT nombre_colonia FROM colonia ORDER BY nombre_colonia")
        self.menu_colonia.configure(values=["Todas las colonias"] + [c["nombre_colonia"] for c in colonias])

    def cargar_datos(self):
        try:
            fecha_desde = texto_a_fecha(self.entry_desde.get())
            fecha_hasta = texto_a_fecha(self.entry_hasta.get())
        except ValueError:
            messagebox.showwarning("Fecha inválida", "Selecciona una fecha válida en el calendario.")
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self._filas_reporte.clear()

        condiciones = ["p.estado_pedido = 'ENTREGADO'"]
        params = []

        if self.controller.id_sucursal_actual:
            condiciones.append("p.id_sucursal = %s")
            params.append(self.controller.id_sucursal_actual)

        if self.var_estado.get() != "Todos los estados":
            condiciones.append("ef.nombre_entidad_fede = %s")
            params.append(self.var_estado.get())

        if self.var_municipio.get() != "Todos los municipios":
            condiciones.append("m.nombre_municipio = %s")
            params.append(self.var_municipio.get())

        if self.var_colonia.get() != "Todas las colonias":
            condiciones.append("c.nombre_colonia = %s")
            params.append(self.var_colonia.get())

        calle = self.entry_calle.get().strip()
        if calle:
            condiciones.append("dir.calle LIKE %s")
            params.append(f"%{calle}%")

        if fecha_desde:
            condiciones.append("DATE(p.fecha_entrega_real) >= %s")
            params.append(fecha_desde)

        if fecha_hasta:
            condiciones.append("DATE(p.fecha_entrega_real) <= %s")
            params.append(fecha_hasta)

        where_sql = " AND ".join(condiciones)

        query = f"""
            SELECT
                ef.nombre_entidad_fede,
                m.nombre_municipio,
                c.nombre_colonia,
                dir.calle,
                COUNT(DISTINCT p.id_pedido) AS pedidos,
                COALESCE(SUM(CASE WHEN pro.tipo_producto = 'GAS_ESTACIONARIO' THEN d.cantidad ELSE 0 END), 0) AS litros,
                COALESCE(SUM(d.cantidad * pr.precio_producto), 0) AS ingresos
            FROM pedido p
            JOIN detalle_pedido d      ON d.id_pedido = p.id_pedido
            JOIN producto pro          ON pro.id_producto = d.id_producto
            JOIN precio_producto pr    ON pr.id_precio = d.id_precio
            JOIN direccion dir         ON dir.id_direccion = p.id_direccion_entrega
            JOIN colonia c             ON c.id_colonia = dir.id_colonia
            JOIN municipio m           ON m.id_municipio = c.id_municipio
            JOIN entidad_federativa ef ON ef.id_entidad_fede = m.id_entidad_fede
            WHERE {where_sql}
            GROUP BY ef.nombre_entidad_fede, m.nombre_municipio, c.nombre_colonia, dir.calle
            ORDER BY ingresos DESC
        """
        filas = self.controller.db.consultar(query, tuple(params))

        suma_ingresos = 0.0
        suma_litros = 0.0
        suma_pedidos = 0

        for f in filas:
            ing = float(f["ingresos"])
            lit = float(f["litros"])
            ped = int(f["pedidos"])
            suma_ingresos += ing
            suma_litros += lit
            suma_pedidos += ped

            fila_formateada = (
                f"{f['nombre_entidad_fede']} / {f['nombre_municipio']}",
                f["nombre_colonia"],
                f["calle"],
                ped,
                f"{lit:,.2f} L",
                f"${ing:,.2f}",
            )
            self._filas_reporte.append(fila_formateada)
            self.tabla.insert("", "end", values=fila_formateada)

        self.lbl_total_ingresos.configure(text=f"${suma_ingresos:,.2f}")
        self.lbl_total_litros.configure(text=f"{suma_litros:,.2f} L")
        self.lbl_total_pedidos.configure(text=str(suma_pedidos))

    def exportar_csv(self):
        if not self._filas_reporte:
            messagebox.showinfo("Sin datos", "No hay registros en la tabla para exportar.")
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar reporte por zona",
            initialfile=f"reporte_zonas_alfagas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            defaultextension=".csv",
            filetypes=[("Archivo CSV (Excel)", "*.csv")]
        )
        if not ruta:
            return

        with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Estado / Municipio", "Colonia", "Calle", "Pedidos", "Litros vendidos", "Total Ingresos"])
            writer.writerows(self._filas_reporte)

        messagebox.showinfo("Reporte exportado", f"Archivo guardado en:\n{ruta}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self._cargar_catalogos()
        self.cargar_datos()