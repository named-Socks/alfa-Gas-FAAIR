from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox


class AjustesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Barra superior verde
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Configuración y ajustes",
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

        # Contenedor principal de las 4 tarjetas
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=40)

        for i in range(4):
            main_frame.grid_columnconfigure(i, weight=1, uniform="cards")

        # --------------------------------------------------------------
        # TARJETA 1: Configuración de precios
        # --------------------------------------------------------------
        card_precio = self._crear_tarjeta(main_frame, 0, "Configuración de precios")

        self.lbl_precio_actual = ctk.CTkLabel(
            card_precio,
            text="Precio actual por litro de gas\n$00.00",
            font=("Arial", 14),
            text_color="#2C3E50",
            justify="center"
        )
        self.lbl_precio_actual.pack(pady=(25, 10))

        fila_nuevo_precio = ctk.CTkFrame(card_precio, fg_color="transparent")
        fila_nuevo_precio.pack(pady=5)
        ctk.CTkLabel(fila_nuevo_precio, text="Nuevo precio: $", font=("Arial", 14), text_color="#2C3E50").pack(side="left")
        self.entry_nuevo_precio = ctk.CTkEntry(fila_nuevo_precio, placeholder_text="00.00", width=85, justify="center")
        self.entry_nuevo_precio.pack(side="left")
        self.entry_nuevo_precio.bind("<Return>", lambda _: self.guardar_nuevo_precio())

        ctk.CTkButton(
            card_precio,
            text="Guardar nuevo precio",
            fg_color="#FFFFFF",
            text_color="#214328",
            border_width=2,
            border_color="#214328",
            hover_color="#E9ECEF",
            font=("Arial", 14, "bold"),
            corner_radius=0,
            command=self.guardar_nuevo_precio
        ).pack(side="bottom", pady=20, padx=20, fill="x")

        # --------------------------------------------------------------
        # TARJETA 2: Conexión con WhatsApp
        # --------------------------------------------------------------
        card_wa = self._crear_tarjeta(main_frame, 1, "Conexión con whatsapp")

        ctk.CTkLabel(
            card_wa,
            text="Número: +52 449 000 00 00\n\nApi key: [**********] 👁️",
            font=("Arial", 14),
            text_color="#2C3E50",
            justify="center"
        ).pack(pady=35)

        # --------------------------------------------------------------
        # TARJETA 3: Seguridad de usuario
        # --------------------------------------------------------------
        card_seg = self._crear_tarjeta(main_frame, 2, "Seguridad de usuario")

        self.lbl_usuario_seg = ctk.CTkLabel(
            card_seg,
            text="Usuario: admin\n\nContraseña: [**********] 👁️",
            font=("Arial", 14),
            text_color="#2C3E50",
            justify="center"
        )
        self.lbl_usuario_seg.pack(pady=35)

        ctk.CTkButton(
            card_seg,
            text="Cambiar contraseña",
            fg_color="#FFFFFF",
            text_color="#214328",
            border_width=2,
            border_color="#214328",
            hover_color="#E9ECEF",
            font=("Arial", 14, "bold"),
            corner_radius=0
        ).pack(side="bottom", pady=20, padx=20, fill="x")

        # --------------------------------------------------------------
        # TARJETA 4: Base de datos local (Respaldo manual)
        # --------------------------------------------------------------
        card_bd = self._crear_tarjeta(main_frame, 3, "Base de datos local")

        self.lbl_ultimo_respaldo = ctk.CTkLabel(
            card_bd,
            text="Último respaldo: 00/00/0000",
            font=("Arial", 14),
            text_color="#2C3E50",
            justify="center",
            wraplength=220
        )
        self.lbl_ultimo_respaldo.pack(pady=40)

        ctk.CTkButton(
            card_bd,
            text="Guardar respaldo",
            fg_color="#FFFFFF",
            text_color="#214328",
            border_width=2,
            border_color="#214328",
            hover_color="#E9ECEF",
            font=("Arial", 14, "bold"),
            corner_radius=0,
            command=self.guardar_respaldo_manual
        ).pack(side="bottom", pady=20, padx=20, fill="x")

    def _crear_tarjeta(self, parent, columna, titulo):
        """Crea la estructura visual uniforme de cada tarjeta."""
        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#BDC3C7",
            width=250,
            height=300
        )
        card.grid(row=0, column=columna, padx=15, pady=20, sticky="nsew")
        card.grid_propagate(False)

        card_header = ctk.CTkFrame(card, fg_color="#214328", corner_radius=0, height=50)
        card_header.pack(fill="x", side="top")
        ctk.CTkLabel(
            card_header,
            text=titulo,
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=12)

        return card

    def _actualizar_datos_pantalla(self):
        """Refresca el precio actual, el usuario y la fecha del último respaldo."""
        precio = self.controller.db.obtener_precio_vigente()
        texto_precio = f"${float(precio):.2f}" if precio is not None else "$00.00"
        self.lbl_precio_actual.configure(text=f"Precio actual por litro de gas\n{texto_precio}")

        usuario = self.controller.admin_actual or "admin"
        self.lbl_usuario_seg.configure(text=f"Usuario: {usuario}\n\nContraseña: [**********] 👁️")

        fecha_respaldo = self.controller.db.obtener_fecha_ultimo_respaldo()
        self.lbl_ultimo_respaldo.configure(
            text=f"Último respaldo:\n{fecha_respaldo}" if fecha_respaldo else "Último respaldo: 00/00/0000"
        )

    def guardar_nuevo_precio(self):
        """Valida el monto ingresado y actualiza el precio vigente en MySQL."""
        texto = self.entry_nuevo_precio.get().strip().replace("$", "").replace(",", ".")
        if not texto:
            messagebox.showwarning("Campo vacío", "Escribe el nuevo precio por litro antes de guardar.")
            return

        try:
            nuevo_precio = round(float(texto), 2)
        except ValueError:
            messagebox.showwarning("Precio inválido", "Ingresa un número válido, por ejemplo: 11.20")
            return

        if nuevo_precio <= 0:
            messagebox.showwarning("Precio inválido", "El precio por litro debe ser mayor a $0.00.")
            return

        exito, mensaje = self.controller.db.actualizar_precio_gas(
            nuevo_precio,
            nombre_admin=self.controller.admin_actual
        )
        if exito:
            self.entry_nuevo_precio.delete(0, "end")
            self._actualizar_datos_pantalla()
            messagebox.showinfo("Precio actualizado", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    def guardar_respaldo_manual(self):
        """Abre el explorador para guardar la copia .sql donde elija el administrador."""
        nombre_sugerido = f"respaldo_alfagas_{datetime.now().strftime('%Y%m%d_%H%M')}.sql"
        ruta = filedialog.asksaveasfilename(
            title="Guardar respaldo de Base de Datos",
            initialdir=self.controller.db.carpeta_respaldos,
            initialfile=nombre_sugerido,
            defaultextension=".sql",
            filetypes=[("Archivo SQL", "*.sql")]
        )
        if not ruta:
            return

        exito, resultado = self.controller.db.generar_respaldo(ruta)
        if exito:
            self._actualizar_datos_pantalla()
            messagebox.showinfo("Respaldo exitoso", f"Copia de seguridad guardada en:\n{resultado}")
        else:
            messagebox.showerror("Error al respaldar", resultado)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self._actualizar_datos_pantalla()