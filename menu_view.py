import customtkinter as ctk

class MenuView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Navbar
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text="🔥 ALFA GAS      Menú de Administrador", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(side="left", padx=30, pady=20)
        self.lbl_admin = ctk.CTkLabel(header, text="", font=("Arial", 14), text_color="#FFFFFF")
        self.lbl_admin.pack(side="right", padx=30)

        # Contenedor central
        card = ctk.CTkFrame(self, fg_color="#F8F9FA", corner_radius=20, width=800, height=450)
        card.pack_propagate(False)
        card.place(relx=0.5, rely=0.5, anchor="center")

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(expand=True)

        botones = [
            ("Clientes", "clientes", 0, 0),
            ("Pedidos", "pedidos", 0, 1),
            ("Reportes\npor zona", "reportes", 0, 2),
            ("Alertas de\npredicción", "alertas", 1, 0),
            ("Historial de\nventas", "historial", 1, 1),
            ("Ajustes", "ajustes", 1, 2)
        ]

        for texto, destino, fila, col in botones:
            btn = ctk.CTkButton(
                grid_frame, text=texto, fg_color="#FFFFFF", text_color="#214328",
                border_width=2, border_color="#214328", hover_color="#E9ECEF",
                font=("Arial", 16, "bold"), width=200, height=80, corner_radius=25,
                command=lambda d=destino: self.controller.mostrar_pantalla(d)
            )
            btn.grid(row=fila, column=col, padx=15, pady=15)

        btn_salir = ctk.CTkButton(
            card, text="Salir", fg_color="#FFFFFF", text_color="#C0392B",
            border_width=2, border_color="#C0392B", hover_color="#FADBD8",
            font=("Arial", 16, "bold"), width=150, height=50, corner_radius=25,
            command=self.cerrar_sesion
        )
        btn_salir.pack(pady=(0, 30))

    def cerrar_sesion(self):
        """Limpia las variables de sesión y regresa al login"""
        self.controller.admin_actual = None
        self.controller.id_sucursal_actual = None
        self.controller.mostrar_pantalla("login")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")