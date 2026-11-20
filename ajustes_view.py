from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox


class ModalCambiarContrasena(ctk.CTkToplevel):
    """Ventana emergente para actualizar la contraseña del administrador."""

    def __init__(self, parent, db, identificador_admin, texto_cuenta):
        super().__init__(parent)
        self.db = db
        self.identificador_admin = identificador_admin

        self.title("Seguridad de usuario - Alfa Gas")
        self.geometry("480x540")
        self.resizable(False, False)
        self.configure(fg_color="#F4F6F7")
        self.transient(parent.winfo_toplevel())

        # Encabezado verde institucional
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=68)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="🔒  Cambiar contraseña",
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=24)

        # Contenedor blanco principal
        card = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#D5DBDB"
        )
        card.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(
            card,
            text=f"Cuenta: {texto_cuenta}",
            font=("Arial", 15, "bold"),
            text_color="#214328"
        ).pack(anchor="w", padx=24, pady=(18, 10))

        self.entry_actual = self._crear_campo_password(card, "Contraseña actual")
        self.entry_nueva = self._crear_campo_password(card, "Nueva contraseña (mínimo 5 caracteres)")
        self.entry_confirmar = self._crear_campo_password(card, "Confirmar nueva contraseña")
        self.entry_confirmar.bind("<Return>", lambda _: self.guardar())

        self.lbl_error = ctk.CTkLabel(
            card,
            text="",
            font=("Arial", 14, "bold"),
            text_color="#C0392B",
            wraplength=390,
            justify="center"
        )
        self.lbl_error.pack(pady=(12, 6), padx=20)

        # Botones inferiores
        fila_botones = ctk.CTkFrame(card, fg_color="transparent")
        fila_botones.pack(fill="x", side="bottom", padx=24, pady=(8, 20))
        fila_botones.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            fila_botones,
            text="Cancelar",
            height=42,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            border_width=1,
            border_color="#BDC3C7",
            hover_color="#E9ECEF",
            font=("Arial", 15, "bold"),
            corner_radius=8,
            command=self.destroy
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            fila_botones,
            text="Guardar contraseña",
            height=42,
            fg_color="#214328",
            text_color="#FFFFFF",
            hover_color="#18321E",
            font=("Arial", 15, "bold"),
            corner_radius=8,
            command=self.guardar
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.after(60, self._centrar_y_enfocar)

    def _crear_campo_password(self, parent, etiqueta):
        """Crea un campo de contraseña con botón de ojito para mostrar/ocultar."""
        ctk.CTkLabel(
            parent,
            text=etiqueta,
            font=("Arial", 15, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", padx=24, pady=(10, 4))

        fila = ctk.CTkFrame(parent, fg_color="transparent")
        fila.pack(fill="x", padx=24)

        entry = ctk.CTkEntry(
            fila,
            height=42,
            font=("Arial", 15),
            corner_radius=8,
            border_color="#BDC3C7",
            show="•"
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        btn_ojo = ctk.CTkButton(
            fila,
            text="👁️",
            width=42,
            height=42,
            font=("Arial", 16),
            corner_radius=8,
            fg_color="#E9ECEF",
            text_color="#2C3E50",
            hover_color="#D5DBDB"
        )
        btn_ojo.configure(command=lambda e=entry, b=btn_ojo: self._alternar_visibilidad(e, b))
        btn_ojo.pack(side="right")

        return entry

    def _alternar_visibilidad(self, entry, boton):
        """Muestra u oculta el texto escrito en el campo de contraseña."""
        if entry.cget("show") == "•":
            entry.configure(show="")
            boton.configure(fg_color="#D5E8D4")
        else:
            entry.configure(show="•")
            boton.configure(fg_color="#E9ECEF")

    def _centrar_y_enfocar(self):
        """Centra la ventana respecto a la pantalla principal y activa el foco modal."""
        self.update_idletasks()
        master = self.master.winfo_toplevel()
        x = master.winfo_rootx() + (master.winfo_width() - self.winfo_width()) // 2
        y = master.winfo_rooty() + (master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        self.grab_set()
        self.entry_actual.focus_set()

    def guardar(self):
        """Valida los tres campos y actualiza la contraseña en MySQL."""
        actual = self.entry_actual.get()
        nueva = self.entry_nueva.get()
        confirmar = self.entry_confirmar.get()

        if not actual or not nueva or not confirmar:
            self.lbl_error.configure(text="Completa los tres campos antes de guardar.")
            return

        if len(nueva) < 5:
            self.lbl_error.configure(text="La nueva contraseña debe tener al menos 5 caracteres.")
            return

        if nueva != confirmar:
            self.lbl_error.configure(text="La nueva contraseña y su confirmación no coinciden.")
            return

        exito, mensaje = self.db.cambiar_contrasena_admin(
            self.identificador_admin,
            actual,
            nueva
        )
        if exito:
            self.destroy()
            messagebox.showinfo("Contraseña actualizada", mensaje)
        else:
            self.lbl_error.configure(text=mensaje)


class AjustesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._modal_pass = None

        # Barra superior verde
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Configuración y ajustes",
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

        # Área central para mantener las 4 tarjetas centradas y con altura equilibrada
        area_central = ctk.CTkFrame(self, fg_color="transparent")
        area_central.pack(fill="both", expand=True)

        main_frame = ctk.CTkFrame(area_central, fg_color="transparent")
        main_frame.place(relx=0.5, rely=0.48, anchor="center")

        main_frame.grid_rowconfigure(0, weight=1, uniform="cards_row")
        main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cards_col")

        # --------------------------------------------------------------
        # TARJETA 1: Configuración de precios
        # --------------------------------------------------------------
        card_precio = self._crear_tarjeta(main_frame, 0, "Configuración de precios")

        self.lbl_precio_actual = ctk.CTkLabel(
            card_precio,
            text="Precio actual por litro de gas\n$00.00",
            font=("Arial", 16),
            text_color="#2C3E50",
            justify="center"
        )
        self.lbl_precio_actual.pack(pady=(35, 16))

        fila_nuevo_precio = ctk.CTkFrame(card_precio, fg_color="transparent")
        fila_nuevo_precio.pack(pady=6)
        ctk.CTkLabel(
            fila_nuevo_precio,
            text="Nuevo precio: $",
            font=("Arial", 15, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")
        self.entry_nuevo_precio = ctk.CTkEntry(
            fila_nuevo_precio,
            placeholder_text="00.00",
            width=95,
            height=38,
            font=("Arial", 15),
            justify="center"
        )
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
            font=("Arial", 16, "bold"),
            height=46,
            corner_radius=0,
            command=self.guardar_nuevo_precio
        ).pack(side="bottom", pady=24, padx=22, fill="x")

        # --------------------------------------------------------------
        # TARJETA 2: Conexión con WhatsApp
        # --------------------------------------------------------------
        card_wa = self._crear_tarjeta(main_frame, 1, "Conexión con WhatsApp")

        ctk.CTkLabel(
            card_wa,
            text="Número:\n+52 449 000 00 00\n\nApi key:\n[**********] 👁️",
            font=("Arial", 16),
            text_color="#2C3E50",
            justify="center"
        ).pack(pady=(35, 10))

        # --------------------------------------------------------------
        # TARJETA 3: Seguridad de usuario
        # --------------------------------------------------------------
        card_seg = self._crear_tarjeta(main_frame, 2, "Seguridad de usuario")

        self.lbl_usuario_seg = ctk.CTkLabel(
            card_seg,
            text="Usuario:\nadmin\n\nContraseña:\n••••••••••",
            font=("Arial", 16),
            text_color="#2C3E50",
            justify="center",
            wraplength=240
        )
        self.lbl_usuario_seg.pack(pady=(35, 10))

        ctk.CTkButton(
            card_seg,
            text="Cambiar contraseña",
            fg_color="#FFFFFF",
            text_color="#214328",
            border_width=2,
            border_color="#214328",
            hover_color="#E9ECEF",
            font=("Arial", 16, "bold"),
            height=46,
            corner_radius=0,
            command=self.abrir_modal_contrasena
        ).pack(side="bottom", pady=24, padx=22, fill="x")

        # --------------------------------------------------------------
        # TARJETA 4: Base de datos local (Respaldo manual)
        # --------------------------------------------------------------
        card_bd = self._crear_tarjeta(main_frame, 3, "Base de datos local")

        self.lbl_ultimo_respaldo = ctk.CTkLabel(
            card_bd,
            text="Último respaldo:\n00/00/0000",
            font=("Arial", 16),
            text_color="#2C3E50",
            justify="center",
            wraplength=240
        )
        self.lbl_ultimo_respaldo.pack(pady=(35, 10))

        ctk.CTkButton(
            card_bd,
            text="Guardar respaldo",
            fg_color="#FFFFFF",
            text_color="#214328",
            border_width=2,
            border_color="#214328",
            hover_color="#E9ECEF",
            font=("Arial", 16, "bold"),
            height=46,
            corner_radius=0,
            command=self.guardar_respaldo_manual
        ).pack(side="bottom", pady=24, padx=22, fill="x")

    def _crear_tarjeta(self, parent, columna, titulo):
        """Crea las 4 tarjetas con exactamente las mismas dimensiones."""
        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#BDC3C7",
            width=285,
            height=380
        )
        card.grid(row=0, column=columna, padx=12, pady=10, sticky="nsew")
        card.pack_propagate(False)

        card_header = ctk.CTkFrame(card, fg_color="#214328", corner_radius=0, height=58)
        card_header.pack(fill="x", side="top")
        card_header.pack_propagate(False)
        ctk.CTkLabel(
            card_header,
            text=titulo,
            font=("Arial", 17, "bold"),
            text_color="#FFFFFF"
        ).pack(expand=True)

        return card

    def _actualizar_datos_pantalla(self):
        """Refresca el precio actual, el usuario y la fecha del último respaldo."""
        precio = self.controller.db.obtener_precio_vigente()
        texto_precio = f"${float(precio):.2f}" if precio is not None else "$00.00"
        self.lbl_precio_actual.configure(text=f"Precio actual por litro de gas\n{texto_precio}")

        info_admin = self.controller.db.obtener_info_admin(self.controller.admin_actual)
        if info_admin:
            usuario_mostrar = info_admin["nombre_usuario_adm"]
        else:
            usuario_mostrar = self.controller.admin_actual or "admin"

        self.lbl_usuario_seg.configure(
            text=f"Usuario:\n{usuario_mostrar}\n\nContraseña:\n••••••••••"
        )

        fecha_respaldo = self.controller.db.obtener_fecha_ultimo_respaldo()
        self.lbl_ultimo_respaldo.configure(
            text=f"Último respaldo:\n{fecha_respaldo}" if fecha_respaldo else "Último respaldo:\n00/00/0000"
        )

    def abrir_modal_contrasena(self):
        """Abre la ventana emergente para cambiar la contraseña del administrador."""
        if not self.controller.admin_actual:
            messagebox.showwarning("Sesión no detectada", "Inicia sesión nuevamente para cambiar tu contraseña.")
            return

        if self._modal_pass is not None and self._modal_pass.winfo_exists():
            self._modal_pass.focus()
            return

        info_admin = self.controller.db.obtener_info_admin(self.controller.admin_actual)
        if info_admin:
            texto_cuenta = f"{info_admin['nombre_adm']} ({info_admin['nombre_usuario_adm']})"
        else:
            texto_cuenta = self.controller.admin_actual

        self._modal_pass = ModalCambiarContrasena(
            self,
            db=self.controller.db,
            identificador_admin=self.controller.admin_actual,
            texto_cuenta=texto_cuenta
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