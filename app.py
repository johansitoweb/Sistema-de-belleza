import tkinter as tk  
from tkinter import messagebox, ttk  
from tkinter import PhotoImage  
import sqlite3  
from PIL import Image, ImageTk  

class SalonDeBelleza:  
    def __init__(self, root):  
        self.root = root  
        self.root.title("Sistema de Salón de Belleza")  

        # Conexión a la base de datos  
        self.conn = sqlite3.connect('usuarios.db')  
        self.crear_tabla_usuarios()  

        # Pantalla de login  
        self.pantalla_login()  
    
    def crear_tabla_usuarios(self):  
        cursor = self.conn.cursor()  
        cursor.execute('''  
            CREATE TABLE IF NOT EXISTS usuarios (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                username TEXT NOT NULL,  
                password TEXT NOT NULL  
            )  
        ''')  
        self.conn.commit()  
    
    def registrar_usuario(self, username, password):  
        cursor = self.conn.cursor()  
        cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))  
        self.conn.commit()  

    def verificar_usuario(self, username, password):  
        cursor = self.conn.cursor()  
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))  
        return cursor.fetchone() is not None  

    def pantalla_login(self):  
        self.login_frame = tk.Frame(self.root)  
        self.login_frame.pack(padx=20, pady=20)  

        tk.Label(self.login_frame, text="Usuario").grid(row=0, column=0, pady=10)  
        self.username_entry = tk.Entry(self.login_frame)  
        self.username_entry.grid(row=0, column=1, pady=10)  

        tk.Label(self.login_frame, text="Contraseña").grid(row=1, column=0, pady=10)  
        self.password_entry = tk.Entry(self.login_frame, show='*')  
        self.password_entry.grid(row=1, column=1, pady=10)  

        self.boton_login = tk.Button(self.login_frame, text="Iniciar Sesión", command=self.iniciar_sesion, bg='blue', fg='white')  
        self.boton_login.grid(row=2, column=0, columnspan=2)  

        self.boton_registrar = tk.Button(self.login_frame, text="Registrar", command=self.registrar_usuario_frame, bg='green', fg='white')  
        self.boton_registrar.grid(row=3, column=0, columnspan=2)  

    def iniciar_sesion(self):  
        username = self.username_entry.get()  
        password = self.password_entry.get()  

        if self.verificar_usuario(username, password):  
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")  
            self.login_frame.destroy()  
            self.configurar_app()  
        else:  
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")  

    def registrar_usuario_frame(self):  
        self.registro_frame = tk.Frame(self.root)  
        self.registro_frame.pack(padx=20, pady=20)  

        tk.Label(self.registro_frame, text="Nuevo Usuario").grid(row=0, column=0, pady=10)  
        self.nuevo_username_entry = tk.Entry(self.registro_frame)  
        self.nuevo_username_entry.grid(row=0, column=1, pady=10)  

        tk.Label(self.registro_frame, text="Nueva Contraseña").grid(row=1, column=0, pady=10)  
        self.nueva_password_entry = tk.Entry(self.registro_frame, show='*')  
        self.nueva_password_entry.grid(row=1, column=1, pady=10)  

        self.boton_registrar_usuario = tk.Button(self.registro_frame, text="Registrar", command=self.registrar, bg='green', fg='white')  
        self.boton_registrar_usuario.grid(row=2, column=0, columnspan=2)  

    def registrar(self):  
        username = self.nuevo_username_entry.get()  
        password = self.nueva_password_entry.get()  
        self.registrar_usuario(username, password)  
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")  
        self.registro_frame.destroy()  

    def configurar_app(self):  
        # Crear el Notebook (pestañas)  
        self.notebook = ttk.Notebook(self.root)  
        self.notebook.pack(fill='both', expand=True)  

        # Pestaña de "Agregar Cita"  
        self.tab_agregar = ttk.Frame(self.notebook)  
        self.notebook.add(self.tab_agregar, text='Agregar Cita')  

        # Pestaña de "Ver Citas"  
        self.tab_ver = ttk.Frame(self.notebook)  
        self.notebook.add(self.tab_ver, text='Ver Citas')  

        # Inicializar lista de citas  
        self.citas = []  

        # Crear entrada para "Agregar Cita"  
        self.crear_tab_agregar()  
        # Crear label para "Ver Citas"  
        self.crear_tab_ver()  
    
    def crear_tab_agregar(self):  
        tk.Label(self.tab_agregar, text="Nombre del Cliente").grid(row=0, column=0, padx=10, pady=10)  
        self.nombre = tk.Entry(self.tab_agregar)  
        self.nombre.grid(row=0, column=1, padx=10, pady=10)  

        tk.Label(self.tab_agregar, text="Servicio").grid(row=1, column=0, padx=10, pady=10)  
        self.servicio = tk.Entry(self.tab_agregar)  
        self.servicio.grid(row=1, column=1, padx=10, pady=10)  

        tk.Label(self.tab_agregar, text="Fecha y Hora").grid(row=2, column=0, padx=10, pady=10)  
        self.fecha_hora = tk.Entry(self.tab_agregar)  
        self.fecha_hora.grid(row=2, column=1, padx=10, pady=10)  

        # Botón para agregar cita  
        self.boton_agregar = tk.Button(self.tab_agregar, text="Agregar Cita", command=self.agregar_cita, bg='blue', fg='white')  
        self.boton_agregar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)  

    def crear_tab_ver(self):  
        self.lista_citas = tk.Listbox(self.tab_ver)  
        self.lista_citas.pack(fill='both', expand=True, padx=10, pady=10)  

    def agregar_cita(self):  
        nombre = self.nombre.get()  
        servicio = self.servicio.get()  
        fecha_hora = self.fecha_hora.get()  

        if nombre and servicio and fecha_hora:  
            cita = f"{nombre} - {servicio} - {fecha_hora}"  
            self.citas.append(cita)  
            self.lista_citas.insert(tk.END, cita)  # Agregar la cita a la lista en la pestaña "Ver Citas"  
            messagebox.showinfo("Éxito", "Cita agregada correctamente.")  
            self.nombre.delete(0, tk.END)  
            self.servicio.delete(0, tk.END)  
            self.fecha_hora.delete(0, tk.END)  
        else:  
            messagebox.showerror("Error", "Por favor, complete todos los campos.")  

if __name__ == "__main__":  
    root = tk.Tk()  
    app = SalonDeBelleza(root)  
    root.mainloop()