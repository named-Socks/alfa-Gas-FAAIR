import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, texto_a_fecha

class HistorialView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text="🔥 ALFA GAS      Historial de ventas", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(side="left", padx=30, pady=20)
        ctk.CTkButton(header, text="Regresar a inicio 🏠", fg_color="#F8F9FA", text_color="#214328", hover_color="#E2E6EA", font=("Arial", 14, "bold"), corner_radius=20, command=lambda: self.controller.mostrar_pantalla("menu")).pack(side="right", padx=30)
        self.lbl_admin = ctk.CTkLabel(header, text="", font=("Arial", 14), text_color="#FFFFFF")
        self.lbl_admin.pack(side="right", padx=10)

        self.lbl_precio = ctk.CTkLabel(self, text="Precio por litro: $00.00", font=("Arial", 14, "bold"), text_color="#7F8C8D")
        self.lbl_precio.place(relx=0.5, rely=0.07, anchor="center")

        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(30, 20))

        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(top_frame, text="Filtros rápidos", font=("Arial", 14, "bold"), text_color="#7F8C8D").pack(side="left")
        ctk.CTkOptionMenu(top_frame, values=["Método de pago"], width=150, fg_color="#FFFFFF", text_color="#2C3E50", button_color="#D5DBDB").pack(side="left", padx=(10, 30))

        ctk.CTkLabel(top_frame, text="Filtro por fecha     Desde", font=("Arial", 14, "bold"), text_color="#7F8C8D").pack(side="left")
        self.entry_desde = ctk.CTkEntry(top_frame, placeholder_text="00/00/0000", width=100)
        self.entry_desde.pack(side="left", padx=5)
        ctk.CTkLabel(top_frame, text="Hasta", font=("Arial", 14, "bold"), text_color="#7F8C8D").pack(side="left", padx=5)
        self.entry_hasta = ctk.CTkEntry(top_frame, placeholder_text="00/00/0000", width=100)
        self.entry_hasta.pack(side="left", padx=5)

        # Botones limpiar(🔄) y buscar(🔍)
        ctk.CTkButton(top_frame, text="🔄", width=40, fg_color="#F5CBA7", text_color="#000", command=self.limpiar_filtros).pack(side="left", padx=2)
        ctk.CTkButton(top_frame, text="🔍", width=40, fg_color="#ABEBC6", text_color="#000", command=self.cargar_datos).pack(side="left", padx=2)

        self.entry_busqueda = ctk.CTkEntry(top_frame, placeholder_text="🔍 Buscar por nombre / folio", width=250, corner_radius=20)
        self.entry_busqueda.pack(side="right")
        self.entry_busqueda.bind("<KeyRelease>", lambda event: self.cargar_datos())

        columnas = ("id", "nombre", "litros", "metodo", "monto")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        encabezados = ["Folio", "Nombre", "Litros surtidos", "Método de pago", "Monto total"]
        for col, texto in zip(columnas, encabezados):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=20, pady=20)

    def limpiar_filtros(self):
        """Vacía las fechas y el buscador y recarga todo el historial"""
        self.entry_desde.delete(0, "end")
        self.entry_hasta.delete(0, "end")
        self.entry_busqueda.delete(0, "end")
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

        sucursal = self.controller.id_sucursal_actual
        query = """
            SELECT folio, cliente, tipo_producto, cantidad, subtotal, fecha_venta
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

        texto = self.entry_busqueda.get().strip()
        if texto:
            query += " AND (cliente LIKE %s OR folio LIKE %s)"
            params += [f"%{texto}%", f"%{texto}%"]

        query += " ORDER BY fecha_venta DESC"

        for fila in self.controller.db.consultar(query, params):
            unidad = "L" if fila["tipo_producto"] == "GAS_ESTACIONARIO" else "pzas"
            self.tabla.insert("", "end", values=(
                fila["folio"],
                fila["cliente"],
                f"{fila['cantidad']} {unidad}",
                "—",  # la base de datos aún no guarda método de pago
                f"${fila['subtotal']}"
            ))

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()