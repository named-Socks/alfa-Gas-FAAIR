import customtkinter as ctk
from tkinter import ttk
from database import BaseDatosLocal
from login_view import LoginView
from menu_view import MenuView
from clientes_view import ClientesView
from alertas_view import AlertasView
from pedidos_view import PedidosView
from historial_view import HistorialView
from reportes_view import ReportesView
from ajustes_view import AjustesView

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class AlfaGasApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Alfa Gas - Sistema Administrativo")
        self.geometry("1200x800")
        self.configure(fg_color="#E9ECEF")

        # Variables de sesión y BD
        self.db = BaseDatosLocal()
        self.admin_actual = None          
        self.id_sucursal_actual = None    

        self.configurar_estilo_tablas()

        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True)

        self.vistas = {}
        self.registrar_vistas()
        self.mostrar_pantalla("login")

    def configurar_estilo_tablas(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 10), rowheight=35, background="#FFFFFF", fieldbackground="#FFFFFF", borderwidth=0)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#214328", foreground="#FFFFFF", borderwidth=1, relief="solid")
        style.map("Treeview", background=[("selected", "#D4E6D9")])

    def registrar_vistas(self):
        clases_vistas = {
            "login": LoginView,
            "menu": MenuView,
            "clientes": ClientesView,
            "alertas": AlertasView,
            "pedidos": PedidosView,
            "historial": HistorialView,
            "reportes": ReportesView,
            "ajustes": AjustesView
        }
        for nombre, ClaseVista in clases_vistas.items():
            vista = ClaseVista(parent=self.contenedor, controller=self)
            self.vistas[nombre] = vista
            vista.grid(row=0, column=0, sticky="nsew")

        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

    def mostrar_pantalla(self, nombre_pantalla):
        vista = self.vistas.get(nombre_pantalla)
        if vista:
            vista.tkraise()

if __name__ == "__main__":
    app = AlfaGasApp()
    app.mainloop()