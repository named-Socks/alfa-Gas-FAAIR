from datetime import date
import customtkinter as ctk
from tkinter import ttk
from database import formatear_fecha, armar_direccion


class AlertasView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._predicciones_cache = {}

        # Barra superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Alertas de predicción",
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

        # Barra superior de filtros
        barra = ctk.CTkFrame(main_frame, fg_color="transparent")
        barra.pack(fill="x", padx=20, pady=(18, 8))

        ctk.CTkLabel(barra, text="Urgencia:", font=("Arial", 15, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 10))
        self.var_urgencia = ctk.StringVar(value="Todas")
        ctk.CTkOptionMenu(
            barra,
            variable=self.var_urgencia,
            values=["Todas", "Crítica / Vencida", "Hoy", "Próximos 3 días", "En tiempo"],
            width=205,
            height=38,
            font=("Arial", 14),
            dropdown_font=("Arial", 14),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        ).pack(side="left")

        # Contenedor de tabla con barras de desplazamiento
        tabla_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=15)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal")

        columnas = ("id_pred", "cliente", "telefono", "direccion", "fecha_agot", "cantidad_est", "prob", "urgencia", "notif")
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
            "ID", "Cliente", "Teléfono", "Dirección",
            "Agotamiento est.", "Cantidad est.", "Probabilidad", "Prioridad", "Último aviso"
        ]
        anchos = [65, 200, 140, 260, 175, 145, 140, 160, 150]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho, minwidth=ancho)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self._predicciones_cache.clear()

        condiciones = ["pr.vigente = 1"]
        params = []
        if self.controller.id_sucursal_actual:
            condiciones.append("c.id_sucursal = %s")
            params.append(self.controller.id_sucursal_actual)

        where_sql = " AND ".join(condiciones)

        query = f"""
            SELECT
                pr.id_prediccion,
                pr.id_cliente,
                c.nombre_cliente,
                c.telefono_whatsapp_cliente,
                d.calle,
                d.num_exterior,
                col.nombre_colonia,
                pr.fecha_estimada_agotamiento,
                pr.cantidad_estimada,
                pr.probabilidad,
                (
                    SELECT n.estado_envio
                    FROM notificacion n
                    WHERE n.id_prediccion = pr.id_prediccion
                    ORDER BY n.id_notificacion DESC
                    LIMIT 1
                ) AS estado_notif
            FROM prediccion pr
            JOIN cliente c ON c.id_cliente = pr.id_cliente
            LEFT JOIN direccion d ON d.id_cliente = c.id_cliente AND d.direccion_recurrente_cliente = 1
            LEFT JOIN colonia col ON col.id_colonia = d.id_colonia
            WHERE {where_sql}
            ORDER BY pr.fecha_estimada_agotamiento ASC
        """
        filas = self.controller.db.consultar(query, tuple(params))
        hoy = date.today()
        filtro_urg = self.var_urgencia.get()

        for f in filas:
            fecha_ag = f["fecha_estimada_agotamiento"]
            dias_restantes = (fecha_ag - hoy).days if fecha_ag else 99

            if dias_restantes < 0:
                urgencia = "Crítica / Vencida"
            elif dias_restantes == 0:
                urgencia = "Hoy"
            elif dias_restantes <= 3:
                urgencia = "Próximos 3 días"
            else:
                urgencia = "En tiempo"

            if filtro_urg != "Todas" and urgencia != filtro_urg:
                continue

            self._predicciones_cache[str(f["id_prediccion"])] = f
            cant_txt = f"{float(f['cantidad_estimada']):.0f} L" if f["cantidad_estimada"] else "—"
            prob_txt = f"{float(f['probabilidad']):.1f}%" if f["probabilidad"] is not None else "—"

            self.tabla.insert(
                "",
                "end",
                iid=str(f["id_prediccion"]),
                values=(
                    f["id_prediccion"],
                    f["nombre_cliente"],
                    f["telefono_whatsapp_cliente"],
                    armar_direccion(f["calle"], f["num_exterior"], f["nombre_colonia"]),
                    formatear_fecha(fecha_ag),
                    cant_txt,
                    prob_txt,
                    urgencia,
                    f["estado_notif"] or "SIN_ENVIAR",
                ),
            )

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()