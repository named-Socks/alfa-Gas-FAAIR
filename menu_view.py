import tkinter as tk
import customtkinter as ctk
from PIL import Image


class MenuView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Navbar superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")

        img_icono = Image.open("/home/jayb/Documentos/GitHub/alfa-Gas-FAAIR/alfaGasIcono.png")
        self.icono_alfa = ctk.CTkImage(light_image=img_icono, dark_image=img_icono, size=(209, 71.33))

        ctk.CTkLabel(
            header,
            image=self.icono_alfa,
            text="   Menú de Administrador",
            compound="left",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=35, pady=22)

        self.lbl_admin = ctk.CTkLabel(
            header,
            text="",
            font=("Arial", 16, "bold"),
            text_color="#FFFFFF"
        )
        self.lbl_admin.pack(side="right", padx=35)

        # Contenedor principal estilo tarjeta suave
        card = ctk.CTkFrame(
            self,
            fg_color="#F7F8F6",
            corner_radius=24,
            border_width=1,
            border_color="#DCDFE0"
        )
        card.pack(fill="both", expand=True, padx=48, pady=34)

        ctk.CTkLabel(
            card,
            text="Selecciona un módulo para administrar",
            font=("Arial", 17, "bold"),
            text_color="#4A5568"
        ).pack(pady=(24, 10))

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=42, pady=(8, 12))

        grid_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="menu_cols")
        grid_frame.grid_rowconfigure((0, 1), weight=1, uniform="menu_rows")

        # (titulo, tipo_icono, destino, fila, col, color_marco, color_borde, color_hover)
        modulos = [
            ("Clientes", "clientes", "clientes", 0, 0, "#E2ECE4", "#8EA392", "#F4F8F5"),
            ("Pedidos", "pedidos", "pedidos", 0, 1, "#E2ECE4", "#8EA392", "#F4F8F5"),
            ("Reportes por zona", "reportes", "reportes", 0, 2, "#E2ECE4", "#8EA392", "#F4F8F5"),
            ("Alertas de predicción", "alertas", "alertas", 1, 0, "#E2ECE4", "#8EA392", "#F4F8F5"),
            ("Historial de ventas", "historial", "historial", 1, 1, "#DCECF7", "#89B0C9", "#F2F8FC"),
            ("Ajustes", "ajustes", "ajustes", 1, 2, "#E3E5E8", "#959A9E", "#F4F5F6"),
        ]

        for titulo, icono, destino, fila, col, bg_marco, borde_marco, bg_hover in modulos:
            self._crear_tarjeta_modulo(
                grid_frame,
                titulo=titulo,
                tipo_icono=icono,
                destino=destino,
                fila=fila,
                col=col,
                bg_marco=bg_marco,
                borde_marco=borde_marco,
                bg_hover=bg_hover
            )

        btn_salir = ctk.CTkButton(
            card,
            text="Salir 🚪",
            fg_color="#FFFFFF",
            text_color="#A94438",
            border_width=1,
            border_color="#A94438",
            hover_color="#FDEDEC",
            font=("Arial", 16, "bold"),
            width=190,
            height=48,
            corner_radius=24,
            command=self.cerrar_sesion
        )
        btn_salir.pack(pady=(6, 24))

    def _crear_tarjeta_modulo(self, parent, titulo, tipo_icono, destino, fila, col, bg_marco, borde_marco, bg_hover):
        # Marco exterior tintado (doble borde como en el diseño)
        outer = ctk.CTkFrame(
            parent,
            fg_color=bg_marco,
            corner_radius=18,
            border_width=1,
            border_color=borde_marco,
            cursor="hand2"
        )
        outer.grid(row=fila, column=col, padx=14, pady=12, sticky="nsew")

        # Tarjeta interior blanca
        inner = ctk.CTkFrame(
            outer,
            fg_color="#FFFFFF",
            corner_radius=13,
            border_width=1,
            border_color="#E5E8E8",
            cursor="hand2"
        )
        inner.pack(fill="both", expand=True, padx=9, pady=9)

        # Contenedor centrado para ícono + texto
        contenido = ctk.CTkFrame(inner, fg_color="transparent", cursor="hand2")
        contenido.place(relx=0.5, rely=0.5, anchor="center")

        canvas = tk.Canvas(
            contenido,
            width=86,
            height=74,
            bg="#FFFFFF",
            highlightthickness=0,
            cursor="hand2"
        )
        canvas.pack(pady=(0, 8))
        self._dibujar_icono(canvas, tipo_icono)

        lbl_titulo = ctk.CTkLabel(
            contenido,
            text=titulo,
            font=("Arial", 19, "bold"),
            text_color="#1C2833",
            cursor="hand2"
        )
        lbl_titulo.pack()

        def al_entrar(_event):
            inner.configure(fg_color=bg_hover)
            canvas.configure(bg=bg_hover)

        def al_salir(event):
            widget_bajo_cursor = self.winfo_containing(event.x_root, event.y_root)
            if widget_bajo_cursor is not None:
                actual = widget_bajo_cursor
                while actual is not None:
                    if actual == outer:
                        return
                    actual = getattr(actual, "master", None)
            inner.configure(fg_color="#FFFFFF")
            canvas.configure(bg="#FFFFFF")

        def al_clic(_event):
            self.controller.mostrar_pantalla(destino)

        for widget in (outer, inner, contenido, canvas, lbl_titulo):
            widget.bind("<Enter>", al_entrar)
            widget.bind("<Leave>", al_salir)
            widget.bind("<Button-1>", al_clic)

    def _dibujar_icono(self, c, tipo):
        if tipo == "clientes":
            # Persona secundaria (derecha, azul más claro)
            c.create_oval(47, 16, 65, 34, fill="#42A5F5", outline="")
            c.create_arc(40, 36, 74, 64, start=0, extent=180, fill="#42A5F5", outline="")
            # Persona principal (izquierda, azul intenso)
            c.create_oval(23, 12, 45, 34, fill="#1E88E5", outline="")
            c.create_arc(14, 36, 54, 68, start=0, extent=180, fill="#1E88E5", outline="")

        elif tipo == "pedidos":
            # Caja isométrica verde
            c.create_polygon(43, 8, 72, 22, 43, 36, 14, 22, fill="#6BB56A", outline="")
            c.create_polygon(14, 22, 43, 36, 43, 66, 14, 52, fill="#438542", outline="")
            c.create_polygon(43, 36, 72, 22, 72, 52, 43, 66, fill="#559E54", outline="")
            # Cinta superior
            c.create_polygon(28, 15, 34, 12, 62, 26, 56, 29, fill="#346B33", outline="")

        elif tipo == "reportes":
            # Gráfica de barras ascendentes verde-azul
            barras = [
                (16, 40, 27, 64, "#8BC34A"),
                (31, 20, 42, 64, "#5CB85C"),
                (46, 30, 57, 64, "#26A69A"),
                (61, 12, 72, 64, "#29B6F6"),
            ]
            for x1, y1, x2, y2, color in barras:
                c.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        elif tipo == "alertas":
            # Rayos de alerta
            rayos = [
                (43, 4, 43, 12),
                (22, 12, 28, 18),
                (64, 12, 58, 18),
                (14, 28, 22, 30),
                (72, 28, 64, 30),
            ]
            for x1, y1, x2, y2 in rayos:
                c.create_line(x1, y1, x2, y2, fill="#FF7043", width=3, capstyle="round")
            # Domo rojo de sirena
            c.create_arc(25, 16, 61, 56, start=0, extent=180, fill="#E53935", outline="")
            c.create_rectangle(25, 35, 61, 54, fill="#E53935", outline="")
            c.create_line(32, 24, 32, 46, fill="#FFCDD2", width=3, capstyle="round")
            # Base gris oscura
            c.create_rectangle(19, 54, 67, 64, fill="#455A64", outline="")

        elif tipo == "historial":
            # Hoja de documento azul claro
            c.create_rectangle(20, 8, 66, 64, fill="#D6EAF8", outline="#85C1E9", width=1)
            # Gráfica circular pequeña
            c.create_oval(26, 14, 40, 28, fill="#2E86C1", outline="")
            c.create_arc(26, 14, 40, 28, start=0, extent=110, fill="#5DADE2", outline="")
            # Líneas de texto
            c.create_line(45, 18, 60, 18, fill="#2E86C1", width=3)
            c.create_line(45, 24, 57, 24, fill="#5DADE2", width=2)
            c.create_line(26, 35, 60, 35, fill="#5DADE2", width=2)
            c.create_line(26, 42, 54, 42, fill="#5DADE2", width=2)
            # Barras inferiores
            c.create_rectangle(27, 51, 31, 59, fill="#2E86C1", outline="")
            c.create_rectangle(34, 48, 38, 59, fill="#2E86C1", outline="")
            c.create_rectangle(41, 53, 45, 59, fill="#5DADE2", outline="")

        elif tipo == "ajustes":
            # Engranaje gris
            cx, cy = 43, 37
            dientes = [
                (39, 10, 47, 64),
                (16, 33, 70, 41),
            ]
            for x1, y1, x2, y2 in dientes:
                c.create_rectangle(x1, y1, x2, y2, fill="#4F5D6B", outline="")
            # Dientes diagonales
            c.create_polygon(22, 21, 28, 15, 64, 51, 58, 57, fill="#4F5D6B", outline="")
            c.create_polygon(58, 15, 64, 21, 28, 57, 22, 51, fill="#4F5D6B", outline="")
            # Cuerpo central del engrane
            c.create_oval(cx - 19, cy - 19, cx + 19, cy + 19, fill="#4F5D6B", outline="")
            c.create_oval(cx - 12, cy - 12, cx + 12, cy + 12, fill="#7F8C8D", outline="")
            c.create_oval(cx - 7, cy - 7, cx + 7, cy + 7, fill="#FFFFFF", outline="")

    def cerrar_sesion(self):
        """Limpia las variables de sesión y regresa al login."""
        self.controller.admin_actual = None
        self.controller.id_sucursal_actual = None
        self.controller.mostrar_pantalla("login")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")