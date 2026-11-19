import customtkinter as ctk
from tkinter import ttk, messagebox
from database import formatear_fecha, armar_direccion


# ==============================================================================
# VENTANA EMERGENTE (MODAL) PARA AGREGAR O MODIFICAR UN CLIENTE
# ==============================================================================
class FormularioClienteModal(ctk.CTkToplevel):
    def __init__(self, parent, db, id_sucursal_admin=None, id_cliente=None, on_guardado=None):
        super().__init__(parent)
        self.db = db
        self.id_sucursal_admin = id_sucursal_admin
        self.id_cliente = id_cliente  # None = Alta nueva | int = Modificar existente
        self.id_direccion = None
        self.on_guardado = on_guardado

        # Mapas de texto -> ID para los menús desplegables
        self.map_sucursales = {}
        self.map_entidades = {}
        self.map_municipios = {}
        self.map_colonias = {}

        # Configuración visual de la ventana modal
        es_edicion = self.id_cliente is not None
        self.title("Modificar Cliente - Alfa Gas" if es_edicion else "Agregar Nuevo Cliente - Alfa Gas")
        self.geometry("680x670")
        self.resizable(False, False)
        self.configure(fg_color="#E9ECEF")

        # Hacerla modal respecto a la ventana principal
        self.transient(parent.winfo_toplevel())
        self.grab_set()
        self.centrar_ventana(680, 670)

        # Encabezado verde institucional
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=65)
        header.pack(fill="x", side="top")
        titulo_header = (
            f"✏️ Modificar información del cliente #{self.id_cliente}"
            if es_edicion
            else "➕ Dar de alta nuevo cliente"
        )
        ctk.CTkLabel(
            header,
            text=titulo_header,
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=25, pady=18)

        # Contenedor desplazable por si la pantalla de la laptop es baja
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#FFFFFF", corner_radius=15)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(15, 10))
        self.scroll.grid_columnconfigure(0, weight=1)
        self.scroll.grid_columnconfigure(1, weight=1)

        self.construir_formulario()
        self.cargar_catalogos()

        if es_edicion:
            self.cargar_datos_cliente()

        # Barra inferior de botones (Cancelar / Guardar)
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=(5, 18))

        ctk.CTkButton(
            footer,
            text="Cancelar",
            fg_color="#FFFFFF",
            text_color="#C0392B",
            border_width=2,
            border_color="#C0392B",
            hover_color="#FADBD8",
            font=("Arial", 14, "bold"),
            width=150,
            height=42,
            corner_radius=12,
            command=self.destroy
        ).pack(side="left")

        texto_guardar = "💾 Guardar cambios" if es_edicion else "💾 Registrar cliente"
        ctk.CTkButton(
            footer,
            text=texto_guardar,
            fg_color="#214328",
            hover_color="#18321E",
            text_color="#FFFFFF",
            font=("Arial", 14, "bold"),
            width=210,
            height=42,
            corner_radius=12,
            command=self.guardar
        ).pack(side="right")

    def centrar_ventana(self, ancho, alto):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def construir_formulario(self):
        # --- SECCIÓN 1: DATOS DEL CLIENTE ---
        ctk.CTkLabel(
            self.scroll,
            text="1. Datos generales del cliente",
            font=("Arial", 15, "bold"),
            text_color="#214328"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(12, 8))

        # Nombre completo
        ctk.CTkLabel(self.scroll, text="Nombre completo *", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(4, 2)
        )
        self.entry_nombre = ctk.CTkEntry(
            self.scroll,
            placeholder_text="Ej. María Guadalupe López",
            height=38,
            corner_radius=10
        )
        self.entry_nombre.grid(row=2, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 10))

        # Teléfono WhatsApp
        ctk.CTkLabel(self.scroll, text="Teléfono WhatsApp (10 dígitos) *", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=3, column=0, sticky="w", padx=15, pady=(4, 2)
        )
        self.entry_telefono = ctk.CTkEntry(
            self.scroll,
            placeholder_text="Ej. 4491234567",
            height=38,
            corner_radius=10
        )
        self.entry_telefono.grid(row=4, column=0, sticky="ew", padx=(15, 8), pady=(0, 10))

        # Estatus del cliente
        ctk.CTkLabel(self.scroll, text="Estatus del cliente *", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=3, column=1, sticky="w", padx=(8, 15), pady=(4, 2)
        )
        self.combo_estado_cliente = ctk.CTkOptionMenu(
            self.scroll,
            values=["ACTIVO", "PENDIENTE_REGISTRO", "INACTIVO", "BAJA"],
            height=38,
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#214328",
            button_hover_color="#18321E"
        )
        self.combo_estado_cliente.set("ACTIVO")
        self.combo_estado_cliente.grid(row=4, column=1, sticky="ew", padx=(8, 15), pady=(0, 10))

        # Sucursal asignada
        ctk.CTkLabel(self.scroll, text="Sucursal *", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=5, column=0, sticky="w", padx=15, pady=(4, 2)
        )
        self.combo_sucursal = ctk.CTkOptionMenu(
            self.scroll,
            values=["Cargando..."],
            height=38,
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#214328",
            button_hover_color="#18321E"
        )
        self.combo_sucursal.grid(row=6, column=0, sticky="ew", padx=(15, 8), pady=(0, 12))

        # Checkbox acepta notificaciones
        self.chk_notificaciones = ctk.CTkCheckBox(
            self.scroll,
            text="Acepta recordatorios por WhatsApp",
            font=("Arial", 13, "bold"),
            text_color="#2C3E50",
            fg_color="#214328",
            hover_color="#18321E"
        )
        self.chk_notificaciones.select()
        self.chk_notificaciones.grid(row=6, column=1, sticky="w", padx=(8, 15), pady=(0, 12))

        # Separador visual
        ctk.CTkFrame(self.scroll, height=2, fg_color="#E9ECEF").grid(
            row=7, column=0, columnspan=2, sticky="ew", padx=15, pady=8
        )

        # --- SECCIÓN 2: DIRECCIÓN DE ENTREGA ---
        ctk.CTkLabel(
            self.scroll,
            text="2. Dirección principal de entrega",
            font=("Arial", 15, "bold"),
            text_color="#214328"
        ).grid(row=8, column=0, columnspan=2, sticky="w", padx=15, pady=(6, 8))

        # Estado (entidad federativa) y Municipio
        ctk.CTkLabel(self.scroll, text="Estado *", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=9, column=0, sticky="w", padx=15, pady=(4, 2)
        )
        self.combo_entidad = ctk.CTkOptionMenu(
            self.scroll,
            values=["Sin registros"],
            height=38,
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#214328",
            button_hover_color="#18321E",
            command=self.al_cambiar_entidad
        )
        self.combo_entidad.grid(row=10, column=0, sticky="ew", padx=(15, 8), pady=(0, 10))

        ctk.CTkLabel(self.scroll, text="Municipio / Ciudad *", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=9, column=1, sticky="w", padx=(8, 15), pady=(4, 2)
        )
        self.combo_municipio = ctk.CTkOptionMenu(
            self.scroll,
            values=["Sin registros"],
            height=38,
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#214328",
            button_hover_color="#18321E",
            command=self.al_cambiar_municipio
        )
        self.combo_municipio.grid(row=10, column=1, sticky="ew", padx=(8, 15), pady=(0, 10))

        # Colonia
        ctk.CTkLabel(self.scroll, text="Colonia *", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=11, column=0, columnspan=2, sticky="w", padx=15, pady=(4, 2)
        )
        self.combo_colonia = ctk.CTkOptionMenu(
            self.scroll,
            values=["Sin registros"],
            height=38,
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#214328",
            button_hover_color="#18321E"
        )
        self.combo_colonia.grid(row=12, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 10))

        # Calle
        ctk.CTkLabel(self.scroll, text="Calle *", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=13, column=0, columnspan=2, sticky="w", padx=15, pady=(4, 2)
        )
        self.entry_calle = ctk.CTkEntry(
            self.scroll,
            placeholder_text="Ej. Av. Francisco I. Madero",
            height=38,
            corner_radius=10
        )
        self.entry_calle.grid(row=14, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 10))

        # Número exterior y Número interior
        ctk.CTkLabel(self.scroll, text="Número exterior *", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=15, column=0, sticky="w", padx=15, pady=(4, 2)
        )
        self.entry_num_ext = ctk.CTkEntry(
            self.scroll,
            placeholder_text="Ej. 104",
            height=38,
            corner_radius=10
        )
        self.entry_num_ext.grid(row=16, column=0, sticky="ew", padx=(15, 8), pady=(0, 10))

        ctk.CTkLabel(self.scroll, text="Número interior (opcional)", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=15, column=1, sticky="w", padx=(8, 15), pady=(4, 2)
        )
        self.entry_num_int = ctk.CTkEntry(
            self.scroll,
            placeholder_text="Ej. B o Depto 2",
            height=38,
            corner_radius=10
        )
        self.entry_num_int.grid(row=16, column=1, sticky="ew", padx=(8, 15), pady=(0, 10))

        # Referencias
        ctk.CTkLabel(self.scroll, text="Referencias del domicilio (opcional)", font=("Arial", 13, "bold"), text_color="#2C3E50").grid(
            row=17, column=0, columnspan=2, sticky="w", padx=15, pady=(4, 2)
        )
        self.entry_referencias = ctk.CTkEntry(
            self.scroll,
            placeholder_text="Ej. Portón verde frente a la tienda",
            height=38,
            corner_radius=10
        )
        self.entry_referencias.grid(row=18, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 15))

    # ------------------------------------------------------------------
    # Carga de catálogos desde MySQL
    # ------------------------------------------------------------------
    def cargar_catalogos(self):
        # 1. Sucursales
        sucursales = self.db.obtener_sucursales()
        self.map_sucursales.clear()
        if sucursales:
            opciones_suc = []
            preseleccion = None
            for s in sucursales:
                etiqueta = f"{s['nombre_sucursal']} ({s['clave_sucursal']})"
                self.map_sucursales[etiqueta] = s["id_sucursal"]
                opciones_suc.append(etiqueta)
                if self.id_sucursal_admin and s["id_sucursal"] == self.id_sucursal_admin:
                    preseleccion = etiqueta
            self.combo_sucursal.configure(values=opciones_suc)
            self.combo_sucursal.set(preseleccion or opciones_suc[0])
            if self.id_sucursal_admin and preseleccion:
                self.combo_sucursal.configure(state="disabled")
        else:
            self.combo_sucursal.configure(values=["Sin sucursales activas"])
            self.combo_sucursal.set("Sin sucursales activas")

        # 2. Entidades federativas -> Municipios -> Colonias
        entidades = self.db.obtener_entidades()
        self.map_entidades.clear()
        if entidades:
            opciones_ent = []
            for e in entidades:
                etiqueta = e["nombre_entidad_fede"]
                self.map_entidades[etiqueta] = e["id_entidad_fede"]
                opciones_ent.append(etiqueta)
            self.combo_entidad.configure(values=opciones_ent)
            self.combo_entidad.set(opciones_ent[0])
            self.al_cambiar_entidad(opciones_ent[0])
        else:
            self.combo_entidad.configure(values=["Sin estados registrados"])
            self.combo_entidad.set("Sin estados registrados")
            self.combo_municipio.configure(values=["Sin municipios"])
            self.combo_municipio.set("Sin municipios")
            self.combo_colonia.configure(values=["Sin colonias"])
            self.combo_colonia.set("Sin colonias")

    def al_cambiar_entidad(self, nombre_entidad):
        id_entidad = self.map_entidades.get(nombre_entidad)
        municipios = self.db.obtener_municipios(id_entidad)
        self.map_municipios.clear()
        if municipios:
            opciones_mun = []
            for m in municipios:
                etiqueta = m["nombre_municipio"]
                self.map_municipios[etiqueta] = m["id_municipio"]
                opciones_mun.append(etiqueta)
            self.combo_municipio.configure(values=opciones_mun)
            self.combo_municipio.set(opciones_mun[0])
            self.al_cambiar_municipio(opciones_mun[0])
        else:
            self.combo_municipio.configure(values=["Sin municipios"])
            self.combo_municipio.set("Sin municipios")
            self.map_colonias.clear()
            self.combo_colonia.configure(values=["Sin colonias"])
            self.combo_colonia.set("Sin colonias")

    def al_cambiar_municipio(self, nombre_municipio):
        id_municipio = self.map_municipios.get(nombre_municipio)
        colonias = self.db.obtener_colonias(id_municipio)
        self.map_colonias.clear()
        if colonias:
            opciones_col = []
            for c in colonias:
                etiqueta = f"{c['nombre_colonia']} (CP {c['codigo_postal']})"
                self.map_colonias[etiqueta] = c["id_colonia"]
                opciones_col.append(etiqueta)
            self.combo_colonia.configure(values=opciones_col)
            self.combo_colonia.set(opciones_col[0])
        else:
            self.combo_colonia.configure(values=["Sin colonias"])
            self.combo_colonia.set("Sin colonias")

    # ------------------------------------------------------------------
    # Precarga de datos cuando se abre en modo "Modificar cliente"
    # ------------------------------------------------------------------
    def cargar_datos_cliente(self):
        cliente = self.db.obtener_cliente_por_id(self.id_cliente)
        if not cliente:
            messagebox.showerror("Error", "No se encontró la información del cliente en la base de datos.", parent=self)
            self.destroy()
            return

        self.id_direccion = cliente["id_direccion"]

        self.entry_nombre.insert(0, cliente["nombre_cliente"] or "")
        self.entry_telefono.insert(0, cliente["telefono_whatsapp_cliente"] or "")
        self.combo_estado_cliente.set(cliente["estado_cliente"] or "ACTIVO")

        if cliente["acepta_notificaciones"]:
            self.chk_notificaciones.select()
        else:
            self.chk_notificaciones.deselect()

        # Seleccionar sucursal correspondiente
        for etiqueta, id_suc in self.map_sucursales.items():
            if id_suc == cliente["id_sucursal"]:
                self.combo_sucursal.set(etiqueta)
                break

        # Seleccionar ubicación geográfica en cascada
        if cliente["nombre_entidad_fede"] and cliente["nombre_entidad_fede"] in self.map_entidades:
            self.combo_entidad.set(cliente["nombre_entidad_fede"])
            self.al_cambiar_entidad(cliente["nombre_entidad_fede"])

        if cliente["nombre_municipio"] and cliente["nombre_municipio"] in self.map_municipios:
            self.combo_municipio.set(cliente["nombre_municipio"])
            self.al_cambiar_municipio(cliente["nombre_municipio"])

        if cliente["id_colonia"]:
            for etiqueta, id_col in self.map_colonias.items():
                if id_col == cliente["id_colonia"]:
                    self.combo_colonia.set(etiqueta)
                    break

        if cliente["calle"]:
            self.entry_calle.insert(0, cliente["calle"])
        if cliente["num_exterior"]:
            self.entry_num_ext.insert(0, cliente["num_exterior"])
        if cliente["num_interior"]:
            self.entry_num_int.insert(0, cliente["num_interior"])
        if cliente["referencias"]:
            self.entry_referencias.insert(0, cliente["referencias"])

    # ------------------------------------------------------------------
    # Validación y guardado en MySQL
    # ------------------------------------------------------------------
    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        estado_cliente = self.combo_estado_cliente.get()
        acepta_notif = 1 if self.chk_notificaciones.get() == 1 else 0

        id_sucursal = self.map_sucursales.get(self.combo_sucursal.get())
        id_colonia = self.map_colonias.get(self.combo_colonia.get())
        calle = self.entry_calle.get().strip()
        num_ext = self.entry_num_ext.get().strip()
        num_int = self.entry_num_int.get().strip()
        referencias = self.entry_referencias.get().strip()

        # Validaciones de campos obligatorios
        if not nombre:
            messagebox.showwarning("Campo obligatorio", "Escribe el nombre completo del cliente.", parent=self)
            self.entry_nombre.focus()
            return

        if not telefono.isdigit() or len(telefono) != 10:
            messagebox.showwarning(
                "Teléfono inválido",
                "El teléfono de WhatsApp debe tener exactamente 10 dígitos numéricos (ej. 4491234567).",
                parent=self
            )
            self.entry_telefono.focus()
            return

        if not id_sucursal:
            messagebox.showwarning(
                "Sin sucursal",
                "No hay una sucursal válida seleccionada. Verifica que exista al menos una sucursal activa en la base de datos.",
                parent=self
            )
            return

        if not id_colonia:
            messagebox.showwarning(
                "Colonia requerida",
                "Selecciona un Estado, Municipio y Colonia válidos. Si las listas aparecen vacías, registra primero el catálogo geográfico en la base de datos.",
                parent=self
            )
            return

        if not calle:
            messagebox.showwarning("Campo obligatorio", "Escribe el nombre de la calle.", parent=self)
            self.entry_calle.focus()
            return

        if not num_ext:
            messagebox.showwarning("Campo obligatorio", "Escribe el número exterior del domicilio.", parent=self)
            self.entry_num_ext.focus()
            return

        datos_cliente = {
            "id_sucursal": id_sucursal,
            "nombre_cliente": nombre,
            "telefono_whatsapp_cliente": telefono,
            "estado_cliente": estado_cliente,
            "acepta_notificaciones": acepta_notif
        }
        datos_direccion = {
            "id_colonia": id_colonia,
            "calle": calle,
            "num_exterior": num_ext,
            "num_interior": num_int,
            "referencias": referencias
        }

        if self.id_cliente is None:
            exito, mensaje = self.db.registrar_cliente(datos_cliente, datos_direccion)
        else:
            exito, mensaje = self.db.actualizar_cliente(
                self.id_cliente, self.id_direccion, datos_cliente, datos_direccion
            )

        if exito:
            messagebox.showinfo("Operación exitosa", mensaje, parent=self)
            if self.on_guardado:
                self.on_guardado()
            self.destroy()
        else:
            messagebox.showerror("No se pudo guardar", mensaje, parent=self)


# ==============================================================================
# PANTALLA PRINCIPAL DE CLIENTES Y PREDICCIONES
# ==============================================================================
class ClientesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Mapas para filtros rápidos geográficos
        self.map_filtro_entidad = {}
        self.map_filtro_municipio = {}
        self.map_filtro_colonia = {}

        # Encabezado verde con título y botón para volver al menú de inicio
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(
            header,
            text="🔥 ALFA GAS      Clientes y predicciones",
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

        # Marco blanco contenedor principal del módulo
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Buscador por nombre o teléfono (se filtra al escribir)
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(15, 0))

        ctk.CTkLabel(
            search_frame,
            text="Filtros rápidos",
            font=("Arial", 14, "bold"),
            text_color="#7F8C8D"
        ).pack(side="left", anchor="s")

        self.entry_busqueda = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar por nombre o teléfono",
            width=300,
            corner_radius=20
        )
        self.entry_busqueda.pack(side="right")
        self.entry_busqueda.bind("<KeyRelease>", lambda event: self.cargar_datos())

        # Barra de filtros geográficos + botones de Agregar / Modificar cliente
        filtros_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=20, pady=10)

        self.combo_filtro_estado = ctk.CTkOptionMenu(
            filtros_frame,
            values=["Estado: Todos"],
            width=135,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=self.al_filtrar_estado
        )
        self.combo_filtro_estado.pack(side="left", padx=(0, 8))

        self.combo_filtro_ciudad = ctk.CTkOptionMenu(
            filtros_frame,
            values=["Ciudad: Todas"],
            width=135,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=self.al_filtrar_ciudad
        )
        self.combo_filtro_ciudad.pack(side="left", padx=(0, 8))

        self.combo_filtro_colonia = ctk.CTkOptionMenu(
            filtros_frame,
            values=["Colonia: Todas"],
            width=145,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.combo_filtro_colonia.pack(side="left", padx=(0, 8))

        self.entry_filtro_calle = ctk.CTkEntry(
            filtros_frame,
            placeholder_text="Calle...",
            width=120
        )
        self.entry_filtro_calle.pack(side="left", padx=(0, 6))
        self.entry_filtro_calle.bind("<KeyRelease>", lambda event: self.cargar_datos())

        ctk.CTkButton(
            filtros_frame,
            text="🔄",
            width=36,
            fg_color="#F5CBA7",
            hover_color="#F0B27A",
            text_color="#000000",
            command=self.limpiar_filtros
        ).pack(side="left", padx=(0, 10))

        # Botón para dar de alta manualmente un cliente nuevo
        ctk.CTkButton(
            filtros_frame,
            text="➕ Agregar cliente",
            fg_color="#214328",
            text_color="#FFFFFF",
            hover_color="#18321E",
            font=("Arial", 13, "bold"),
            height=34,
            command=self.abrir_ventana_agregar
        ).pack(side="right")

        # Botón para modificar el cliente seleccionado en la tabla
        ctk.CTkButton(
            filtros_frame,
            text="✏️ Modificar cliente",
            fg_color="#E9F7EF",
            text_color="#214328",
            border_width=1,
            border_color="#214328",
            hover_color="#D4EFDF",
            font=("Arial", 13, "bold"),
            height=34,
            command=self.abrir_ventana_modificar_seleccionado
        ).pack(side="right", padx=(0, 10))

        # Tabla con la lista de clientes, hábitos de consumo y botón de acción al lado
        columnas = ("id", "nombre", "telefono", "direccion", "promedio", "proximo", "estatus", "editar")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings", selectmode="browse")
        encabezados = [
            "ID", "Nombre", "Teléfono", "Dirección",
            "Promedio de\nconsumo", "Próximo consumo", "Estatus", "Acción"
        ]
        anchos = [50, 160, 105, 250, 115, 130, 110, 110]
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Eventos de clic en la celda "✏️ Modificar" o doble clic en la fila
        self.tabla.bind("<ButtonRelease-1>", self.al_hacer_clic_tabla)
        self.tabla.bind("<Double-1>", self.al_doble_clic_tabla)
        self.tabla.bind("<Motion>", self.al_mover_mouse_tabla)

    # ------------------------------------------------------------------
    # Apertura de ventanas de Alta y Modificación
    # ------------------------------------------------------------------
    def abrir_ventana_agregar(self):
        FormularioClienteModal(
            parent=self,
            db=self.controller.db,
            id_sucursal_admin=self.controller.id_sucursal_actual,
            id_cliente=None,
            on_guardado=self.cargar_datos
        )

    def abrir_ventana_modificar(self, id_cliente):
        FormularioClienteModal(
            parent=self,
            db=self.controller.db,
            id_sucursal_admin=self.controller.id_sucursal_actual,
            id_cliente=int(id_cliente),
            on_guardado=self.cargar_datos
        )

    def abrir_ventana_modificar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo(
                "Selecciona un cliente",
                "Primero selecciona un cliente de la tabla (o haz clic directo en '✏️ Modificar' en su fila)."
            )
            return
        valores = self.tabla.item(seleccion[0], "values")
        if valores:
            self.abrir_ventana_modificar(valores[0])

    def al_hacer_clic_tabla(self, event):
        """Detecta si el usuario hizo clic en la columna '✏️ Modificar' al lado de la info del cliente"""
        region = self.tabla.identify("region", event.x, event.y)
        if region != "cell":
            return
        columna = self.tabla.identify_column(event.x)
        fila_id = self.tabla.identify_row(event.y)
        # "#8" corresponde a la 8va columna ("editar")
        if columna == "#8" and fila_id:
            valores = self.tabla.item(fila_id, "values")
            if valores:
                self.abrir_ventana_modificar(valores[0])

    def al_doble_clic_tabla(self, event):
        fila_id = self.tabla.identify_row(event.y)
        if fila_id:
            valores = self.tabla.item(fila_id, "values")
            if valores:
                self.abrir_ventana_modificar(valores[0])

    def al_mover_mouse_tabla(self, event):
        """Cambia el cursor a mano cuando pasa sobre la columna '✏️ Modificar'"""
        region = self.tabla.identify("region", event.x, event.y)
        columna = self.tabla.identify_column(event.x)
        if region == "cell" and columna == "#8":
            self.tabla.configure(cursor="hand2")
        else:
            self.tabla.configure(cursor="")

    # ------------------------------------------------------------------
    # Filtros geográficos rápidos
    # ------------------------------------------------------------------
    def cargar_opciones_filtros(self):
        self.map_filtro_entidad.clear()
        opciones_est = ["Estado: Todos"]
        for e in self.controller.db.obtener_entidades():
            self.map_filtro_entidad[e["nombre_entidad_fede"]] = e["id_entidad_fede"]
            opciones_est.append(e["nombre_entidad_fede"])
        self.combo_filtro_estado.configure(values=opciones_est)
        if self.combo_filtro_estado.get() not in opciones_est:
            self.combo_filtro_estado.set("Estado: Todos")

        self.cargar_opciones_ciudad()
        self.cargar_opciones_colonia()

    def cargar_opciones_ciudad(self):
        id_ent = self.map_filtro_entidad.get(self.combo_filtro_estado.get())
        self.map_filtro_municipio.clear()
        opciones_ciu = ["Ciudad: Todas"]
        for m in self.controller.db.obtener_municipios(id_ent):
            self.map_filtro_municipio[m["nombre_municipio"]] = m["id_municipio"]
            opciones_ciu.append(m["nombre_municipio"])
        self.combo_filtro_ciudad.configure(values=opciones_ciu)
        if self.combo_filtro_ciudad.get() not in opciones_ciu:
            self.combo_filtro_ciudad.set("Ciudad: Todas")

    def cargar_opciones_colonia(self):
        id_mun = self.map_filtro_municipio.get(self.combo_filtro_ciudad.get())
        self.map_filtro_colonia.clear()
        opciones_col = ["Colonia: Todas"]
        for c in self.controller.db.obtener_colonias(id_mun):
            self.map_filtro_colonia[c["nombre_colonia"]] = c["id_colonia"]
            opciones_col.append(c["nombre_colonia"])
        self.combo_filtro_colonia.configure(values=opciones_col)
        if self.combo_filtro_colonia.get() not in opciones_col:
            self.combo_filtro_colonia.set("Colonia: Todas")

    def al_filtrar_estado(self, _):
        self.combo_filtro_ciudad.set("Ciudad: Todas")
        self.combo_filtro_colonia.set("Colonia: Todas")
        self.cargar_opciones_ciudad()
        self.cargar_opciones_colonia()
        self.cargar_datos()

    def al_filtrar_ciudad(self, _):
        self.combo_filtro_colonia.set("Colonia: Todas")
        self.cargar_opciones_colonia()
        self.cargar_datos()

    def limpiar_filtros(self):
        self.entry_busqueda.delete(0, "end")
        self.entry_filtro_calle.delete(0, "end")
        self.combo_filtro_estado.set("Estado: Todos")
        self.combo_filtro_ciudad.set("Ciudad: Todas")
        self.combo_filtro_colonia.set("Colonia: Todas")
        self.cargar_opciones_filtros()
        self.cargar_datos()

    # ------------------------------------------------------------------
    # Carga de registros de la tabla desde MySQL
    # ------------------------------------------------------------------
    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        id_ent = self.map_filtro_entidad.get(self.combo_filtro_estado.get())
        id_mun = self.map_filtro_municipio.get(self.combo_filtro_ciudad.get())
        id_col = self.map_filtro_colonia.get(self.combo_filtro_colonia.get())
        calle = self.entry_filtro_calle.get().strip()
        busqueda = self.entry_busqueda.get().strip()

        filas = self.controller.db.obtener_clientes(
            id_sucursal=self.controller.id_sucursal_actual,
            busqueda=busqueda,
            id_entidad=id_ent,
            id_municipio=id_mun,
            id_colonia=id_col,
            calle=calle
        )

        for fila in filas:
            promedio = f"{fila['promedio_dias_consumo']} días" if fila["promedio_dias_consumo"] else "N/A"
            self.tabla.insert("", "end", values=(
                fila["id_cliente"],
                fila["nombre_cliente"],
                fila["telefono_whatsapp_cliente"],
                armar_direccion(
                    fila["calle"],
                    fila["num_exterior"],
                    fila["colonia"],
                    fila["num_interior"]
                ),
                promedio,
                formatear_fecha(fila["fecha_estimada_agotamiento"]),
                fila["estado_cliente"],
                "✏️ Modificar"
            ))

    # Se ejecuta cada vez que la pantalla pasa al frente: refresca nombre, filtros y tabla
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_opciones_filtros()
        self.cargar_datos()