from datetime import date
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, armar_direccion


class AlertasView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._predicciones_cache = {}

        # Barra superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Alertas de predicción",
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

        # Contenedor principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Barra superior de filtros y botón de acción
        barra = ctk.CTkFrame(main_frame, fg_color="transparent")
        barra.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(barra, text="Urgencia:", font=("Arial", 13, "bold"), text_color="#2C3E50").pack(side="left", padx=(0, 8))
        self.var_urgencia = ctk.StringVar(value="Todas")
        ctk.CTkOptionMenu(
            barra,
            variable=self.var_urgencia,
            values=["Todas", "Crítica / Vencida", "Hoy", "Próximos 3 días", "En tiempo"],
            width=170,
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        ).pack(side="left")

        ctk.CTkButton(
            barra,
            text="📲 Registrar envío de recordatorio",
            fg_color="#214328",
            hover_color="#18321E",
            text_color="#FFFFFF",
            font=("Arial", 13, "bold"),
            corner_radius=10,
            command=self.enviar_recordatorio_seleccionado
        ).pack(side="right")

        # Tabla
        columnas = ("id_pred", "cliente", "telefono", "direccion", "fecha_agot", "cantidad_est", "prob", "urgencia", "notif")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        encabezados = [
            "ID", "Cliente", "Teléfono", "Dirección",
            "Agotamiento est.", "Cantidad est.", "Probabilidad", "Prioridad", "Último aviso"
        ]
        anchos = [45, 165, 105, 220, 110, 100, 95, 125, 115]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho)
        self.tabla.pack(fill="both", expand=True, padx=20, pady=15)

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

    def enviar_recordatorio_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona un cliente", "Elige una fila de la tabla para registrar el recordatorio.")
            return

        id_pred = seleccion[0]
        datos = self._predicciones_cache.get(id_pred)
        if not datos:
            return

        query = """
            INSERT INTO notificacion (
                id_cliente, id_prediccion, id_pedido, tipo_notificacion,
                numero_intento, fecha_programada, fecha_envio,
                estado_envio, resultado_notificacion
            )
            VALUES (%s, %s, NULL, 'RECORDATORIO', 1, NOW(), NOW(), 'ENVIADO', 'SIN_RESPUESTA')
        """
        nuevo_id = self.controller.db.ejecutar(query, (datos["id_cliente"], datos["id_prediccion"]))
        if nuevo_id:
            self.cargar_datos()
            messagebox.showinfo(
                "Recordatorio registrado",
                f"Se registró el envío de recordatorio por WhatsApp para {datos['nombre_cliente']}."
            )
        else:
            messagebox.showerror("Error", "No se pudo registrar la notificación en MySQL.")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()