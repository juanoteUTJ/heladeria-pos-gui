import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="heladeria",
            password="TuPasswordSeguro",
            database="heladeria",
            unix_socket="/var/lib/mysql/mysql.sock"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Conexión fallida: {e}")
        return None

class HeladeriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Heladería POS")
        
        # Pestañas
        self.notebook = ttk.Notebook(root)
        
        # Pestaña Sabores
        self.tab_sabores = ttk.Frame(self.notebook)
        self.setup_sabores_tab()
        self.notebook.add(self.tab_sabores, text="Sabores")
        
        self.notebook.pack(expand=True, fill="both")

    def setup_sabores_tab(self):
        # Contenido simplificado
        tk.Label(self.tab_sabores, text="Nombre:").grid(row=0, column=0)
        self.nombre_entry = tk.Entry(self.tab_sabores)
        self.nombre_entry.grid(row=0, column=1)
        
        tk.Button(self.tab_sabores, text="Guardar", 
                 command=self.guardar_sabor).grid(row=1, columnspan=2)

    def guardar_sabor(self):
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO sabores (nombre) VALUES (%s)", 
                             (self.nombre_entry.get(),))
                conn.commit()
                messagebox.showinfo("Éxito", "Sabor guardado!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HeladeriaApp(root)
    root.mainloop()
