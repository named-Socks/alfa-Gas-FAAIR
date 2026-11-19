import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, texto_a_fecha

class ReportesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text="🔥 ALFA GAS      Reportes de ventas por zona", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(side="left", padx=30, pady=20)
        ctk.CTkButton(header, text="Regresar a inicio 🏠", fg_color="#F8F9FA", text_color="#214328", hover_color="#E2E6EA", font=("Arial", 14, "bold"), corner_radius=20, command=lambda: self.controller.mostrar_pantalla("menu")).pack(side="right", padx=30)
        self.lbl_admin = ctk.CTkLabel(header, text="", font=("Arial", 14), text_color="#FFFFFF")
        self.lbl_admin.pack(side="right", padx=10)

        self.lbl_precio = ctk.CTkLabel(self, text="Precio por litro: $00.00", font=("Arial", 14, "bold"), text_color="#7F8C8D")
        self.lbl_precio.place(relx=0.5, rely=0.07, anchor="center")

        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(30, 20))

        ctk.CTkLabel(main_frame, text="Filtros rápidos", font=("Arial", 14, "bold"), text_color="#7F8C8D").pack(anchor="w", padx=20, pady=(15, 5))
        filtros_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=20)

        for f in ["Estado", "Ciudad", "Colonia", "Calle", "Método de pago"]:
            ctk.CTkOptionMenu(filtros_frame, values=[f], width=120, fg_color="#FFFFFF", text_color="#2C3E50", button_color="#D5DBDB").pack(side="left", padx=(0, 15))

        mid_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        mid_frame.pack(fill="x", padx=20, pady=20)

        resumen_frame = ctk.CTkFrame(mid_frame, fg_color="transparent")
        resumen_frame.pack(side="left")
        ctk.CTkLabel(resumen_frame, text="Resumen general de la zona seleccionada", font=("Arial", 12, "bold"), text_color="#7F8C8D").pack(anchor="w", pady=(0, 5))

        self.tabla_resumen = ttk.Treeview(resumen_frame, columns=("ingresos", "litros", "pedidos"), show="headings", height=1)
        self.tabla_resumen.heading("ingresos", text="Total de Ingresos")
        self.tabla_resumen.heading("litros", text="Total de litros vendidos")
        self.tabla_resumen.heading("pedidos", text="Total de pedidos")
        self.tabla_resumen.pack()

        fecha_frame = ctk.CTkFrame(mid_frame, fg_color="transparent")
        fecha_frame.pack(side="right", anchor="s")
        ctk.CTkLabel(fecha_frame, text="Filtro por fecha", font=("Arial", 12, "bold"), text_color="#7F8C8D").pack(anchor="w")

        cont_fechas = ctk.CTkFrame(fecha_frame, fg_color="transparent")
        cont_fechas.pack()
        ctk.CTkLabel(cont_fechas, text="Desde", font=("Arial", 12, "bold"), text_color="#7F8C8D").pack(side="left", padx=5)
        self.entry_desde = ctk.CTkEntry(cont_fechas, placeholder_text="00/00/0000", width=100)
        self.entry_desde.pack(side="left")
        ctk.CTkLabel(cont_fechas, text="Hasta", font=("Arial", 12, "bold"), text_color="#7F8C8D").pack(side="left", padx=5)
        self.entry_hasta = ctk.CTkEntry(cont_fechas, placeholder_text="00/00/0000", width=100)
        self.entry_hasta.pack(side="left")
        ctk.CTkButton(cont_fechas, text="🔄", width=35, fg_color="#F5CBA7", text_color="#000", command=self.limpiar_filtros).pack(side="left", padx=5)
        ctk.CTkButton(cont_fechas, text="🔍", width=35, fg_color="#ABEBC6", text_color="#000", command=self.cargar_datos).pack(side="left")

        columnas = ("ubicacion", "colonia", "fecha", "pedidos", "litros", "total")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        encabezados = ["Ubicación", "Colonia", "Última venta", "Pedidos", "Litros", "Total Ingresos"]
        for col, texto in zip(columnas, encabezados):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def limpiar_filtros(self):
        self.entry_desde.delete(0, "end")
        self.entry_hasta.delete(0, "end")
        self.cargar_datos()

    def cargar_datos(self):
        try:
            desde = texto_a_fecha(self.entry_desde.get())
            hasta = texto_a_fecha(self.entry_hasta.get())
        except ValueError:
            messagebox.showwarning("Fecha inválida", "Escribe las fechas como dd/mm/aaaa, por ejemplo 28/09/2026.")
            return

        precio = self.controller.db.obtener_precio_vigente()
        self.lbl_precio.configure(text=f"Precio por litro: ${precio}" if precio is not None else "Precio por litro: sin definir")

        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for item in self.tabla_resumen.get_children():
            self.tabla_resumen.delete(item)

        sucursal = self.controller.id_sucursal_actual
        query = """
            SELECT municipio, colonia,
                   COUNT(DISTINCT id_pedido) AS pedidos,
                   SUM(CASE WHEN tipo_producto = 'GAS_ESTACIONARIO' THEN cantidad ELSE 0 END) AS litros,
                   SUM(subtotal) AS total,
                   MAX(fecha_venta) AS ultima_venta
            FROM vw_ventas_detalle
            WHERE (%s IS NULL OR id_sucursal = %s)
        """
        params = [sucursal, sucursal]

        if desde:
            query += " AND DATE(fecha_venta) >= %s"
            params.append(desde)
        if hasta:
            query += " AND DATE(fecha_venta) <= %s"
            params.append(hasta)

        query += " GROUP BY municipio, colonia ORDER BY total DESC"

        total_ingresos = 0
        total_litros = 0
        total_pedidos = 0

        for fila in self.controller.db.consultar(query, params):
            self.tabla.insert("", "end", values=(
                fila["municipio"],
                fila["colonia"],
                formatear_fecha(fila["ultima_venta"]),
                fila["pedidos"],
                f"{fila['litros']} L",
                f"${fila['total']}"
            ))
            total_ingresos += fila["total"] or 0
            total_litros += fila["litros"] or 0
            total_pedidos += fila["pedidos"] or 0

        self.tabla_resumen.insert("", "end", values=(f"${total_ingresos:.2f}", f"{total_litros:.2f} L", total_pedidos))

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()