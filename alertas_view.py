import customtkinter as ctk
from tkinter import ttk
from datetime import date
from database import formatear_fecha, armar_direccion

class AlertasView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text="🔥 ALFA GAS      Alertas y Predicciones de Consumo", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(side="left", padx=30, pady=20)
        ctk.CTkButton(header, text="Regresar a inicio 🏠", fg_color="#F8F9FA", text_color="#214328", hover_color="#E2E6EA", font=("Arial", 14, "bold"), corner_radius=20, command=lambda: self.controller.mostrar_pantalla("menu")).pack(side="right", padx=30)
        self.lbl_admin = ctk.CTkLabel(header, text="", font=("Arial", 14), text_color="#FFFFFF")
        self.lbl_admin.pack(side="right", padx=10)

        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(15, 0))
        self.entry_busqueda = ctk.CTkEntry(search_frame, placeholder_text="🔍 Buscar por nombre", width=300, corner_radius=20)
        self.entry_busqueda.pack(side="right")
        self.entry_busqueda.bind("<KeyRelease>", lambda event: self.cargar_datos())

        ctk.CTkLabel(main_frame, text="Filtros rápidos", font=("Arial", 14, "bold"), text_color="#7F8C8D").pack(anchor="w", padx=20)
        filtros_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=20, pady=10)

        for f in ["Estado", "Ciudad", "Colonia", "Calle", "Estatus"]:
            ctk.CTkOptionMenu(filtros_frame, values=[f], width=120, fg_color="#FFFFFF", text_color="#2C3E50", button_color="#D5DBDB").pack(side="left", padx=(0, 15))

        columnas = ("id", "nombre", "tel", "dir", "prom", "prox", "est_alerta", "est_msg")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        encabezados = ["ID_cliente", "Nombre", "Teléfono", "Dirección", "Promedio de\nconsumo", "Próximo consumo", "Estatus de\nalerta", "Estatus de\nmensaje"]
        for col, texto in zip(columnas, encabezados):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=20, pady=20)

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        sucursal = self.controller.id_sucursal_actual
        # Consulta que trae la predicción vigente y el estado de la última notificación enviada
        query = """
            SELECT c.id_cliente, c.nombre_completo, c.telefono_whatsapp,
                   d.calle, d.num_exterior, col.nombre AS colonia,
                   p.promedio_dias_consumo, p.fecha_estimada_agotamiento,
                   n.estado_envio
            FROM prediccion p
            JOIN cliente c ON c.id_cliente = p.id_cliente
            LEFT JOIN direccion d ON d.id_direccion = c.id_direccion_actual
            LEFT JOIN colonia col ON col.id_colonia = d.id_colonia
            LEFT JOIN notificacion n ON n.id_prediccion = p.id_prediccion
                 AND n.id_notificacion = (SELECT MAX(n2.id_notificacion) FROM notificacion n2 WHERE n2.id_prediccion = p.id_prediccion)
            WHERE p.vigente = 1 AND (%s IS NULL OR c.id_sucursal = %s)
        """
        params = [sucursal, sucursal]

        texto = self.entry_busqueda.get().strip()
        if texto:
            query += " AND c.nombre_completo LIKE %s"
            params.append(f"%{texto}%")

        query += " ORDER BY p.fecha_estimada_agotamiento ASC"

        hoy = date.today()
        for fila in self.controller.db.consultar(query, params):
            dias = (fila["fecha_estimada_agotamiento"] - hoy).days
            if dias < 0:
                estatus_alerta = f"Atrasado ({abs(dias)} d)"
            elif dias == 0:
                estatus_alerta = "Hoy"
            else:
                estatus_alerta = f"En {dias} días"

            self.tabla.insert("", "end", values=(
                fila["id_cliente"],
                fila["nombre_completo"],
                fila["telefono_whatsapp"],
                armar_direccion(fila["calle"], fila["num_exterior"], fila["colonia"]),
                f"{fila['promedio_dias_consumo']} días",
                formatear_fecha(fila["fecha_estimada_agotamiento"]),
                estatus_alerta,
                fila["estado_envio"] or "SIN ENVIAR"
            ))

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()