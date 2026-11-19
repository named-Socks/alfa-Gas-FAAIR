import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Navbar
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text="🔥 ALFA GAS      Inicio de sesión", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(side="left", padx=30, pady=20)

        # Contenedor central
        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=20, border_width=2, border_color="#214328", width=400, height=400)
        card.pack_propagate(False)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Campos
        ctk.CTkLabel(card, text="Usuario", font=("Arial", 16, "bold"), text_color="#2C3E50").pack(anchor="w", padx=40, pady=(40, 5))
        self.entry_usuario = ctk.CTkEntry(card, width=320, height=40, corner_radius=10, border_color="#214328")
        self.entry_usuario.pack(padx=40)

        ctk.CTkLabel(card, text="Contraseña", font=("Arial", 16, "bold"), text_color="#2C3E50").pack(anchor="w", padx=40, pady=(20, 5))
        self.entry_pass = ctk.CTkEntry(card, width=320, height=40, corner_radius=10, border_color="#214328", show="*")
        self.entry_pass.pack(padx=40)
        self.entry_pass.bind("<Return>", lambda event: self.procesar_login())  # Permite usar la tecla Enter

        self.lbl_error = ctk.CTkLabel(card, text="", text_color="#C0392B", font=("Arial", 12, "bold"))
        self.lbl_error.pack(pady=10)

        # Botón
        ctk.CTkButton(
            card, text="Ingresar", fg_color="#214328", hover_color="#18321E",
            font=("Arial", 16, "bold"), height=45, corner_radius=10,
            command=self.procesar_login
        ).pack(pady=(10, 20), padx=40, fill="x")

    def procesar_login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_pass.get()

        if not usuario or not contrasena:
            self.lbl_error.configure(text="Escribe tu usuario y contraseña.")
            return

        valido, datos = self.controller.db.verificar_login(usuario, contrasena)
        if valido:
            self.controller.admin_actual = datos["nombre_completo"]
            self.controller.id_sucursal_actual = datos["id_sucursal"]  # None = ve todas las sucursales
            self.lbl_error.configure(text="")
            self.entry_usuario.delete(0, "end")
            self.entry_pass.delete(0, "end")
            self.controller.mostrar_pantalla("menu")
        elif self.controller.db.ultimo_error:
            self.lbl_error.configure(text="No se pudo conectar a la base de datos.")
        else:
            self.lbl_error.configure(text="Usuario o contraseña incorrectos.")