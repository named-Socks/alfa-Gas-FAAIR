import customtkinter as ctk


class MenuView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Navbar superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Menú de Administrador",
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

        # Contenedor principal responsivo
        card = ctk.CTkFrame(self, fg_color="#F8F9FA", corner_radius=24)
        card.pack(fill="both", expand=True, padx=70, pady=50)

        ctk.CTkLabel(
            card,
            text="Selecciona un módulo para administrar",
            font=("Arial", 20, "bold"),
            text_color="#566573"
        ).pack(pady=(30, 10))

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=55, pady=(15, 20))

        grid_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="menu_cols")
        grid_frame.grid_rowconfigure((0, 1), weight=1, uniform="menu_rows")

        botones = [
            ("👥\nClientes", "clientes", 0, 0),
            ("📦\nPedidos", "pedidos", 0, 1),
            ("📊\nReportes por zona", "reportes", 0, 2),
            ("🚨\nAlertas de predicción", "alertas", 1, 0),
            ("🧾\nHistorial de ventas", "historial", 1, 1),
            ("⚙️\nAjustes", "ajustes", 1, 2)
        ]

        for texto, destino, fila, col in botones:
            btn = ctk.CTkButton(
                grid_frame,
                text=texto,
                fg_color="#FFFFFF",
                text_color="#214328",
                border_width=2,
                border_color="#214328",
                hover_color="#E9ECEF",
                font=("Arial", 21, "bold"),
                corner_radius=25,
                command=lambda d=destino: self.controller.mostrar_pantalla(d)
            )
            btn.grid(row=fila, column=col, padx=18, pady=18, sticky="nsew")

        btn_salir = ctk.CTkButton(
            card,
            text="Salir 🚪",
            fg_color="#FFFFFF",
            text_color="#C0392B",
            border_width=2,
            border_color="#C0392B",
            hover_color="#FADBD8",
            font=("Arial", 18, "bold"),
            width=220,
            height=58,
            corner_radius=28,
            command=self.cerrar_sesion
        )
        btn_salir.pack(pady=(5, 35))

    def cerrar_sesion(self):
        """Limpia las variables de sesión y regresa al login."""
        self.controller.admin_actual = None
        self.controller.id_sucursal_actual = None
        self.controller.mostrar_pantalla("login")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")