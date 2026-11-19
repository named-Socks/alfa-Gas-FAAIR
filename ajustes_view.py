# Importación de la librería gráfica
import customtkinter as ctk

# Clase que maneja la pantalla de Configuración y Ajustes técnicos
class AjustesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Encabezado verde institucional con botón para regresar a la pantalla de Menú
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text="🔥 ALFA GAS      Configuración y ajustes", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(side="left", padx=30, pady=20)
        ctk.CTkButton(header, text="Regresar a inicio 🏠", fg_color="#F8F9FA", text_color="#214328", hover_color="#E2E6EA", font=("Arial", 14, "bold"), corner_radius=20, command=lambda: self.controller.mostrar_pantalla("menu")).pack(side="right", padx=30)

        # Contenedor transparente donde se organizan las 4 tarjetas operativas
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=40)

        # Matriz con los datos para armar cada tarjeta: (Título, Texto explicativo, Texto del botón)
        tarjetas_data = [
            ("Configuración de precios", "Precio actual por litro de gas\n$00.00\nNuevo precio: $[ $00.00 ]", "Guardar nuevo precio"),
            ("Conexión con whatsapp", "Número: +52 449 000 00 00\n\nApi key: [**********] 👁️", None),
            ("Seguridad de usuario", "Usuario: Admin_oficina\n\nContraseña: [**********] 👁️", "Cambiar contraseña"),
            ("Base de datos local", "Último respaldo: 00/00/0000\n\n", "Guardar respaldo")
        ]

        # Construcción dinámica de las 4 tarjetas de configuración en una fila horizontal
        for i, (titulo, cuerpo, texto_btn) in enumerate(tarjetas_data):
            card = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", width=250, height=300)
            card.grid(row=0, column=i, padx=15, pady=20, sticky="nsew")
            card.grid_propagate(False)

            # Header verde superior de la tarjeta
            card_header = ctk.CTkFrame(card, fg_color="#214328", corner_radius=0, height=50)
            card_header.pack(fill="x", side="top")
            ctk.CTkLabel(card_header, text=titulo, font=("Arial", 14, "bold"), text_color="#FFFFFF").pack(pady=12)

            # Texto informativo central
            ctk.CTkLabel(card, text=cuerpo, font=("Arial", 14), text_color="#2C3E50", justify="center").pack(pady=30)

            # Botón de acción ubicado en la parte inferior de la tarjeta
            if texto_btn:
                ctk.CTkButton(
                    card, text=texto_btn, fg_color="#FFFFFF", text_color="#214328",
                    border_width=2, border_color="#214328", hover_color="#E9ECEF",
                    font=("Arial", 14, "bold"), corner_radius=0
                ).pack(side="bottom", pady=20, padx=20, fill="x")

        # Configuración para expandir las 4 columnas de forma equitativa
        for i in range(4):
            main_frame.grid_columnconfigure(i, weight=1)