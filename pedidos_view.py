import re
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import armar_direccion
from PIL import Image


class ModalNuevoPedido(ctk.CTkToplevel):
    """Ventana emergente para registrar un pedido manual desde administración."""

    def __init__(self, parent, db, id_sucursal, al_guardar):
        super().__init__(parent)
        self.db = db
        self.id_sucursal = id_sucursal
        self.al_guardar = al_guardar

        self._clientes_map = {}
        self._productos_map = {}
        self._precio_actual = 0.0

        self.title("Nuevo pedido - Alfa Gas")
        self.geometry("540x640")
        self.resizable(False, False)
        self.configure(fg_color="#F4F6F7")
        self.transient(parent.winfo_toplevel())
        self.bind("<Escape>", lambda _: self.destroy())

        # Barra superior
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=76)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="➕  Nuevo pedido manual",
            font=("Arial", 24, "bold"),
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

        # Campo: Cliente
        ctk.CTkLabel(
            card,
            text="Cliente",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", padx=24, pady=(18, 4))

        self.var_cliente = ctk.StringVar(value="Cargando clientes...")
        self.menu_cliente = ctk.CTkOptionMenu(
            card,
            variable=self.var_cliente,
            values=["Cargando clientes..."],
            height=42,
            font=("Arial", 15),
            dropdown_font=("Arial", 15),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=self._al_cambiar_cliente
        )
        self.menu_cliente.pack(fill="x", padx=24)

        # Dirección de entrega (informativa del cliente seleccionado)
        ctk.CTkLabel(
            card,
            text="Dirección de entrega",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", padx=24, pady=(12, 4))

        self.lbl_direccion = ctk.CTkLabel(
            card,
            text="Selecciona un cliente para ver su dirección",
            font=("Arial", 14),
            text_color="#566573",
            fg_color="#F8F9FA",
            corner_radius=8,
            anchor="w",
            padx=12,
            pady=10,
            wraplength=430,
            justify="left"
        )
        self.lbl_direccion.pack(fill="x", padx=24)

        # Campo: Producto
        ctk.CTkLabel(
            card,
            text="Producto",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", padx=24, pady=(12, 4))

        self.var_producto = ctk.StringVar(value="Cargando productos...")
        self.menu_producto = ctk.CTkOptionMenu(
            card,
            variable=self.var_producto,
            values=["Cargando productos..."],
            height=42,
            font=("Arial", 15),
            dropdown_font=("Arial", 15),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=self._al_cambiar_producto
        )
        self.menu_producto.pack(fill="x", padx=24)

        # Fila: Cantidad + Estatus inicial
        fila_cant_est = ctk.CTkFrame(card, fg_color="transparent")
        fila_cant_est.pack(fill="x", padx=24, pady=(12, 0))
        fila_cant_est.grid_columnconfigure((0, 1), weight=1, uniform="cant_est")

        col_cant = ctk.CTkFrame(fila_cant_est, fg_color="transparent")
        col_cant.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.lbl_cantidad = ctk.CTkLabel(
            col_cant,
            text="Cantidad (litros)",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        )
        self.lbl_cantidad.pack(anchor="w", pady=(0, 4))
        self.entry_cantidad = ctk.CTkEntry(
            col_cant,
            height=42,
            font=("Arial", 16),
            placeholder_text="Ej. 120",
            corner_radius=8,
            border_color="#BDC3C7"
        )
        self.entry_cantidad.pack(fill="x")
        self.entry_cantidad.bind("<KeyRelease>", lambda _: self._recalcular_total())
        self.entry_cantidad.bind("<Return>", lambda _: self.guardar())

        col_est = ctk.CTkFrame(fila_cant_est, fg_color="transparent")
        col_est.grid(row=0, column=1, padx=(8, 0), sticky="ew")
        ctk.CTkLabel(
            col_est,
            text="Estatus inicial",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(0, 4))
        self.var_estado = ctk.StringVar(value="REGISTRADO")
        self.menu_estado = ctk.CTkOptionMenu(
            col_est,
            variable=self.var_estado,
            values=["REGISTRADO", "ENTREGADO"],
            height=42,
            font=("Arial", 15),
            dropdown_font=("Arial", 15),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB"
        )
        self.menu_estado.pack(fill="x")

        # Resumen de precio y total estimado
        resumen_box = ctk.CTkFrame(card, fg_color="#EAFAF1", corner_radius=8)
        resumen_box.pack(fill="x", padx=24, pady=(16, 0))

        self.lbl_total = ctk.CTkLabel(
            resumen_box,
            text="Total estimado: $0.00",
            font=("Arial", 17, "bold"),
            text_color="#214328"
        )
        self.lbl_total.pack(pady=10)

        # Mensaje de validación
        self.lbl_error = ctk.CTkLabel(
            card,
            text="",
            font=("Arial", 14, "bold"),
            text_color="#C0392B",
            wraplength=440,
            justify="center"
        )
        self.lbl_error.pack(pady=(10, 4), padx=20)

        # Botones inferiores
        fila_botones = ctk.CTkFrame(card, fg_color="transparent")
        fila_botones.pack(fill="x", side="bottom", padx=24, pady=(8, 20))
        fila_botones.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            fila_botones,
            text="Cancelar",
            height=44,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            border_width=1,
            border_color="#BDC3C7",
            hover_color="#E9ECEF",
            font=("Arial", 16, "bold"),
            corner_radius=8,
            command=self.destroy
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            fila_botones,
            text="Registrar pedido",
            height=44,
            fg_color="#214328",
            text_color="#FFFFFF",
            hover_color="#18321E",
            font=("Arial", 16, "bold"),
            corner_radius=8,
            command=self.guardar
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self._cargar_catalogos()
        self.after(60, self._centrar_y_enfocar)

    def _centrar_y_enfocar(self):
        self.update_idletasks()
        master = self.master.winfo_toplevel()
        x = master.winfo_rootx() + (master.winfo_width() - self.winfo_width()) // 2
        y = master.winfo_rooty() + (master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        self.grab_set()
        self.entry_cantidad.focus_set()

    def _cargar_catalogos(self):
        # 1. Clientes activos con dirección vigente
        sql_clientes = """
            SELECT
                c.id_cliente,
                c.id_sucursal,
                c.nombre_cliente,
                c.telefono_whatsapp_cliente,
                d.id_direccion,
                d.calle,
                d.num_exterior,
                d.num_interior,
                col.nombre_colonia,
                col.codigo_postal,
                m.nombre_municipio,
                ef.nombre_entidad_fede
            FROM cliente c
            INNER JOIN direccion d
                ON d.id_cliente = c.id_cliente AND d.direccion_recurrente_cliente = 1
            INNER JOIN colonia col ON d.id_colonia = col.id_colonia
            INNER JOIN municipio m ON col.id_municipio = m.id_municipio
            INNER JOIN entidad_federativa ef ON m.id_entidad_fede = ef.id_entidad_fede
            WHERE c.estado_cliente IN ('ACTIVO', 'PENDIENTE_REGISTRO')
              AND (%s IS NULL OR c.id_sucursal = %s)
            ORDER BY c.nombre_cliente ASC
        """
        clientes = self.db.consultar(sql_clientes, (self.id_sucursal, self.id_sucursal))
        self._clientes_map.clear()
        opciones_cli = []
        for c in clientes:
            etiqueta = f"{c['nombre_cliente']} ({c['telefono_whatsapp_cliente']})"
            self._clientes_map[etiqueta] = c
            opciones_cli.append(etiqueta)

        if opciones_cli:
            self.menu_cliente.configure(values=opciones_cli)
            self.var_cliente.set(opciones_cli[0])
            self._al_cambiar_cliente(opciones_cli[0])
        else:
            self.menu_cliente.configure(values=["Sin clientes con dirección"])
            self.var_cliente.set("Sin clientes con dirección")
            self.lbl_direccion.configure(text="Registra un cliente con dirección en el módulo Clientes primero.")

        # 2. Productos activos y su precio vigente
        sql_productos = """
            SELECT
                pr.id_producto,
                pr.nombre_producto,
                pr.tipo_producto,
                pp.id_precio,
                pp.precio_producto
            FROM producto pr
            LEFT JOIN precio_producto pp
                ON pp.id_producto = pr.id_producto AND pp.fecha_fin IS NULL
            WHERE pr.activo_producto = 1
            ORDER BY pr.id_producto ASC
        """
        productos = self.db.consultar(sql_productos)
        self._productos_map.clear()
        opciones_prod = []
        for p in productos:
            precio_val = float(p["precio_producto"] or 0)
            etiqueta = f"{p['nombre_producto']} (${precio_val:,.2f})"
            if etiqueta not in self._productos_map:
                self._productos_map[etiqueta] = p
                opciones_prod.append(etiqueta)

        if opciones_prod:
            self.menu_producto.configure(values=opciones_prod)
            self.var_producto.set(opciones_prod[0])
            self._al_cambiar_producto(opciones_prod[0])
        else:
            self.menu_producto.configure(values=["Sin productos activos"])
            self.var_producto.set("Sin productos activos")

    def _al_cambiar_cliente(self, seleccion):
        cli = self._clientes_map.get(seleccion)
        if cli:
            self.lbl_direccion.configure(text=armar_direccion(cli))

    def _al_cambiar_producto(self, seleccion):
        prod = self._productos_map.get(seleccion)
        if prod:
            self._precio_actual = float(prod["precio_producto"] or 0)
            unidad = "litros" if prod["tipo_producto"] == "GAS_ESTACIONARIO" else "piezas"
            self.lbl_cantidad.configure(text=f"Cantidad ({unidad})")
            self._recalcular_total()

    def _recalcular_total(self):
        texto = self.entry_cantidad.get().strip()
        try:
            cant = float(texto)
            if cant > 0:
                total = cant * self._precio_actual
                self.lbl_total.configure(text=f"Total estimado: ${total:,.2f}")
                return
        except ValueError:
            pass
        self.lbl_total.configure(text="Total estimado: $0.00")

    def _generar_siguiente_folio(self, cursor):
        cursor.execute("SELECT folio FROM pedido ORDER BY id_pedido DESC LIMIT 50")
        mayor = 0
        for (folio,) in cursor.fetchall():
            coincidencia = re.search(r"(\d+)$", str(folio or ""))
            if coincidencia:
                mayor = max(mayor, int(coincidencia.group(1)))
        return f"PED-{mayor + 1:04d}"

    def guardar(self):
        cli = self._clientes_map.get(self.var_cliente.get())
        if not cli:
            self.lbl_error.configure(text="Selecciona un cliente válido con dirección registrada.")
            return

        prod = self._productos_map.get(self.var_producto.get())
        if not prod or not prod.get("id_precio"):
            self.lbl_error.configure(text="Selecciona un producto que tenga precio vigente configurado.")
            return

        try:
            cantidad = float(self.entry_cantidad.get().strip())
        except ValueError:
            self.lbl_error.configure(text="Ingresa una cantidad numérica válida (ej. 120).")
            return

        if cantidad <= 0:
            self.lbl_error.configure(text="La cantidad debe ser mayor a cero.")
            return

        estado = self.var_estado.get()
        precio_unit = float(prod["precio_producto"])

        conexion = self.db.conectar()
        if not conexion:
            self.lbl_error.configure(text="No se pudo conectar a la base de datos.")
            return

        cursor = conexion.cursor()
        try:
            folio = self._generar_siguiente_folio(cursor)
            id_suc = cli["id_sucursal"] or self.id_sucursal or 1

            if estado == "ENTREGADO":
                cursor.execute(
                    """
                    INSERT INTO pedido (
                        folio, id_cliente, id_sucursal, id_direccion_entrega,
                        estado_pedido, origen_pedido, fecha_entrega_real
                    )
                    VALUES (%s, %s, %s, %s, %s, 'ADMIN', NOW())
                    """,
                    (folio, cli["id_cliente"], id_suc, cli["id_direccion"], estado)
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO pedido (
                        folio, id_cliente, id_sucursal, id_direccion_entrega,
                        estado_pedido, origen_pedido
                    )
                    VALUES (%s, %s, %s, %s, %s, 'ADMIN')
                    """,
                    (folio, cli["id_cliente"], id_suc, cli["id_direccion"], estado)
                )

            id_pedido = cursor.lastrowid
            cursor.execute(
                """
                INSERT INTO detalle_pedido (
                    id_pedido, id_producto, id_precio, cantidad_litros, precio_unitario
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_pedido, prod["id_producto"], prod["id_precio"], cantidad, precio_unit)
            )

            conexion.commit()
            self.destroy()
            self.al_guardar()
            messagebox.showinfo(
                "Pedido registrado",
                f"El pedido {folio} para {cli['nombre_cliente']} se registró correctamente."
            )
        except Exception as e:
            conexion.rollback()
            self.lbl_error.configure(text=f"Error al registrar pedido en MySQL: {e}")
        finally:
            cursor.close()
            conexion.close()


class PedidosView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.pedidos_map = {}
        self._modal_nuevo = None

        # Navbar unificado
        header = ctk.CTkFrame(self, fg_color="#214328", corner_radius=0, height=88)
        header.pack(fill="x", side="top")

        img_icono = Image.open("/home/jayb/Documentos/GitHub/alfa-Gas-FAAIR/alfaGasIcono.png")
        self.icono_alfa = ctk.CTkImage(light_image=img_icono, dark_image=img_icono, size=(209, 71.33))

        ctk.CTkLabel(
            header,
            image=self.icono_alfa,
            text="   Pedidos",
            compound="left",
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

        self.lbl_precio = ctk.CTkLabel(
            self,
            text="Precio por litro: $00.00",
            font=("Arial", 17, "bold"),
            text_color="#214328"
        )
        self.lbl_precio.pack(pady=(12, 0))

        # Contenedor principal
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Barra de filtros (letra agrandada)
        top_bar = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(18, 8))

        ctk.CTkLabel(
            top_bar,
            text="Filtros rápidos:",
            font=("Arial", 17, "bold"),
            text_color="#2C3E50"
        ).pack(side="left")

        self.combo_estado = ctk.CTkOptionMenu(
            top_bar,
            values=["Todos los estados", "REGISTRADO", "ENTREGADO", "CANCELADO", "FALLIDO"],
            width=215,
            height=44,
            font=("Arial", 16),
            dropdown_font=("Arial", 16),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.combo_estado.pack(side="left", padx=12)

        self.combo_origen = ctk.CTkOptionMenu(
            top_bar,
            values=["Todos los orígenes", "WHATSAPP", "ADMIN"],
            width=215,
            height=44,
            font=("Arial", 16),
            dropdown_font=("Arial", 16),
            fg_color="#F8F9FA",
            text_color="#2C3E50",
            button_color="#D5DBDB",
            command=lambda _: self.cargar_datos()
        )
        self.combo_origen.pack(side="left", padx=8)

        self.entry_busqueda = ctk.CTkEntry(
            top_bar,
            placeholder_text="🔍 Buscar por cliente o folio",
            width=300,
            height=44,
            font=("Arial", 16),
            corner_radius=22
        )
        self.entry_busqueda.pack(side="right")
        self.entry_busqueda.bind("<KeyRelease>", lambda _: self.cargar_datos())

        # Barra de cambio de estatus y nuevo pedido
        accion_bar = ctk.CTkFrame(main_frame, fg_color="#F8F9FA", corner_radius=10)
        accion_bar.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            accion_bar,
            text="Selecciona un pedido y cambia su estatus:",
            font=("Arial", 16, "bold"),
            text_color="#2C3E50"
        ).pack(side="left", padx=16, pady=12)

        self.combo_nuevo_estado = ctk.CTkOptionMenu(
            accion_bar,
            values=["ENTREGADO", "REGISTRADO", "CANCELADO", "FALLIDO"],
            width=185,
            height=42,
            font=("Arial", 16),
            dropdown_font=("Arial", 16),
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            button_color="#D5DBDB"
        )
        self.combo_nuevo_estado.pack(side="left", padx=10)

        ctk.CTkButton(
            accion_bar,
            text="Actualizar estatus ✔",
            fg_color="#214328",
            hover_color="#18321E",
            font=("Arial", 16, "bold"),
            height=42,
            corner_radius=10,
            command=self.cambiar_estatus_pedido
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            accion_bar,
            text="➕ Nuevo pedido",
            fg_color="#214328",
            hover_color="#18321E",
            text_color="#FFFFFF",
            font=("Arial", 16, "bold"),
            height=42,
            corner_radius=10,
            command=self._abrir_modal_nuevo_pedido
        ).pack(side="right", padx=16)

        # Tabla (tamaño de letra sin cambios)
        columnas = ("folio", "fecha", "cliente", "dir", "litros", "monto", "origen", "estatus")
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        encabezados = ["Folio", "Fecha / Hora", "Cliente", "Dirección de entrega", "Cantidad", "Monto total", "Origen", "Estatus"]
        anchos = [95, 145, 190, 290, 110, 115, 105, 115]

        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, anchor="center", width=ancho)

        self.tabla.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    def _abrir_modal_nuevo_pedido(self):
        if self._modal_nuevo is not None and self._modal_nuevo.winfo_exists():
            self._modal_nuevo.focus()
            return

        self._modal_nuevo = ModalNuevoPedido(
            self,
            db=self.controller.db,
            id_sucursal=self.controller.id_sucursal_actual,
            al_guardar=self.cargar_datos
        )

    def cargar_datos(self):
        precio = self.controller.db.obtener_precio_vigente()
        self.lbl_precio.configure(
            text=f"Precio por litro: ${precio:.2f}" if precio is not None else "Precio por litro: sin definir"
        )

        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.pedidos_map.clear()

        sucursal = self.controller.id_sucursal_actual
        query = """
            SELECT
                p.id_pedido,
                p.folio,
                DATE_FORMAT(p.fecha_registro, '%d/%m/%Y %H:%i') AS fecha_fmt,
                c.nombre_cliente,
                d.calle, d.num_exterior, d.num_interior,
                col.nombre_colonia, col.codigo_postal,
                m.nombre_municipio, ef.nombre_entidad_fede,
                COALESCE(SUM(dp.cantidad_litros), 0) AS cantidad_total,
                MAX(pr.tipo_producto) AS tipo_producto,
                COALESCE(SUM(COALESCE(dp.subtotal, dp.cantidad_litros * COALESCE(dp.precio_unitario, pp.precio_producto))), 0) AS monto_total,
                p.origen_pedido,
                p.estado_pedido
            FROM pedido p
            INNER JOIN cliente c ON p.id_cliente = c.id_cliente
            INNER JOIN direccion d ON p.id_direccion_entrega = d.id_direccion
            INNER JOIN colonia col ON d.id_colonia = col.id_colonia
            INNER JOIN municipio m ON col.id_municipio = m.id_municipio
            INNER JOIN entidad_federativa ef ON m.id_entidad_fede = ef.id_entidad_fede
            INNER JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
            INNER JOIN producto pr ON dp.id_producto = pr.id_producto
            LEFT JOIN precio_producto pp ON dp.id_precio = pp.id_precio
            WHERE (%s IS NULL OR p.id_sucursal = %s)
        """
        params = [sucursal, sucursal]

        estado = self.combo_estado.get()
        if estado != "Todos los estados":
            query += " AND p.estado_pedido = %s"
            params.append(estado)

        origen = self.combo_origen.get()
        if origen != "Todos los orígenes":
            query += " AND p.origen_pedido = %s"
            params.append(origen)

        texto = self.entry_busqueda.get().strip()
        if texto:
            query += " AND (c.nombre_cliente LIKE %s OR p.folio LIKE %s)"
            params += [f"%{texto}%", f"%{texto}%"]

        query += """
            GROUP BY p.id_pedido, p.folio, p.fecha_registro, c.nombre_cliente,
                     d.calle, d.num_exterior, d.num_interior, col.nombre_colonia,
                     col.codigo_postal, m.nombre_municipio, ef.nombre_entidad_fede,
                     p.origen_pedido, p.estado_pedido
            ORDER BY p.fecha_registro DESC
        """

        for fila in self.controller.db.consultar(query, params):
            unidad = "L" if fila["tipo_producto"] == "GAS_ESTACIONARIO" else "pzas"
            direccion_txt = armar_direccion(fila)
            item_id = self.tabla.insert("", "end", values=(
                fila["folio"],
                fila["fecha_fmt"],
                fila["nombre_cliente"],
                direccion_txt,
                f"{float(fila['cantidad_total']):.2f} {unidad}",
                f"${float(fila['monto_total']):,.2f}",
                fila["origen_pedido"],
                fila["estado_pedido"]
            ))
            self.pedidos_map[item_id] = fila["id_pedido"]

    def cambiar_estatus_pedido(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Primero haz clic sobre un pedido en la tabla.")
            return

        id_pedido = self.pedidos_map.get(seleccion[0])
        nuevo_estado = self.combo_nuevo_estado.get()

        if nuevo_estado == "ENTREGADO":
            sql = "UPDATE pedido SET estado_pedido = %s, fecha_entrega_real = NOW() WHERE id_pedido = %s"
        else:
            sql = "UPDATE pedido SET estado_pedido = %s WHERE id_pedido = %s"

        self.controller.db.ejecutar(sql, (nuevo_estado, id_pedido))
        self.cargar_datos()
        messagebox.showinfo("Actualizado", f"El pedido cambió a estatus: {nuevo_estado}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if self.controller.admin_actual:
            self.lbl_admin.configure(text=f"👤 {self.controller.admin_actual}")
        self.cargar_datos()