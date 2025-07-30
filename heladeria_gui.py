import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# --- CONEXIÓN A MYSQL ---
def conectar_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  # Cambia esto
            database="heladeria",
            unix_socket="/var/lib/mysql/mysql.sock"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión: {str(e)}")
        return None

# --- CLASE PRINCIPAL ---
class HeladeriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Heladería POS")
        self.root.geometry("1000x700")
        
        # Configura el estilo
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=('Arial', 10))
        
        # Notebook (Pestañas)
        self.notebook = ttk.Notebook(root)
        
        # Pestaña Sabores
        self.tab_sabores = ttk.Frame(self.notebook)
        self.setup_sabores_tab()
        
        # Pestaña Ventas
        self.tab_ventas = ttk.Frame(self.notebook)
        self.setup_ventas_tab()
        
        # Pestaña Reportes
        self.tab_reportes = ttk.Frame(self.notebook)
        self.setup_reportes_tab()
        
        self.notebook.add(self.tab_sabores, text="Sabores")
        self.notebook.add(self.tab_ventas, text="Ventas")
        self.notebook.add(self.tab_reportes, text="Reportes")
        self.notebook.pack(expand=True, fill="both")

    # --- PESTAÑA SABORES ---
    def setup_sabores_tab(self):
        # Frame del formulario
        form_frame = ttk.LabelFrame(self.tab_sabores, text="Registrar Nuevo Sabor", padding=10)
        form_frame.pack(pady=10, padx=10, fill="x")
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.nombre_sabor = ttk.Entry(form_frame, width=30)
        self.nombre_sabor.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Precio ($):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.precio_sabor = ttk.Entry(form_frame, width=10)
        self.precio_sabor.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(form_frame, text="Stock:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.stock_sabor = ttk.Spinbox(form_frame, from_=0, to=1000, width=8)
        self.stock_sabor.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Botón Guardar
        ttk.Button(
            form_frame,
            text="Guardar Sabor",
            command=self.registrar_sabor
        ).grid(row=3, columnspan=2, pady=10)
        
        # Tabla de sabores
        tree_frame = ttk.Frame(self.tab_sabores)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.tree_sabores = ttk.Treeview(
            tree_frame,
            columns=("id", "nombre", "precio", "stock"),
            show="headings",
            height=15
        )
        
        # Configurar columnas
        self.tree_sabores.heading("id", text="ID")
        self.tree_sabores.heading("nombre", text="Nombre")
        self.tree_sabores.heading("precio", text="Precio ($)")
        self.tree_sabores.heading("stock", text="Stock")
        
        self.tree_sabores.column("id", width=50, anchor="center")
        self.tree_sabores.column("nombre", width=200)
        self.tree_sabores.column("precio", width=100, anchor="e")
        self.tree_sabores.column("stock", width=80, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_sabores.yview)
        self.tree_sabores.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_sabores.pack(fill="both", expand=True)
        
        self.actualizar_lista_sabores()

    def registrar_sabor(self):
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO sabores (nombre, precio, stock) VALUES (%s, %s, %s)",
                    (self.nombre_sabor.get(), float(self.precio_sabor.get()), int(self.stock_sabor.get()))
                conn.commit()
                messagebox.showinfo("Éxito", "Sabor registrado correctamente!")
                self.nombre_sabor.delete(0, tk.END)
                self.precio_sabor.delete(0, tk.END)
                self.stock_sabor.delete(0, tk.END)
                self.actualizar_lista_sabores()
            except ValueError:
                messagebox.showerror("Error", "Precio y Stock deben ser números válidos")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar: {str(e)}")
            finally:
                conn.close()

    def actualizar_lista_sabores(self):
        for item in self.tree_sabores.get_children():
            self.tree_sabores.delete(item)
        
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM sabores ORDER BY nombre")
                for sabor in cursor.fetchall():
                    self.tree_sabores.insert("", "end", values=(
                        sabor["id"],
                        sabor["nombre"],
                        f"{sabor['precio']:.2f}",
                        sabor["stock"]
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar sabores: {str(e)}")
            finally:
                conn.close()

    # --- PESTAÑA VENTAS ---
    def setup_ventas_tab(self):
        # Frame izquierdo (Selección)
        left_frame = ttk.Frame(self.tab_ventas)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Sabores disponibles
        ttk.Label(left_frame, text="Sabores Disponibles:", font=('Arial', 10, 'bold')).pack(pady=5)
        
        self.lista_sabores = tk.Listbox(left_frame, width=30, height=15, selectmode="single")
        self.lista_sabores.pack(pady=5)
        
        # Botón para agregar a la venta
        ttk.Button(
            left_frame,
            text="Agregar a Venta",
            command=self.agregar_a_venta
        ).pack(pady=10)
        
        # Frame derecho (Venta actual)
        right_frame = ttk.Frame(self.tab_ventas)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Venta Actual:", font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Tabla de items en venta
        self.tree_venta = ttk.Treeview(
            right_frame,
            columns=("sabor", "precio"),
            show="headings",
            height=10
        )
        self.tree_venta.heading("sabor", text="Sabor")
        self.tree_venta.heading("precio", text="Precio ($)")
        self.tree_venta.column("sabor", width=200)
        self.tree_venta.column("precio", width=100, anchor="e")
        self.tree_venta.pack(fill="both", expand=True, pady=5)
        
        # Total
        self.total_venta = tk.DoubleVar(value=0.0)
        ttk.Label(
            right_frame,
            textvariable=self.total_venta,
            font=('Arial', 12, 'bold'),
            foreground="green"
        ).pack(pady=10)
        
        # Botón Finalizar Venta
        ttk.Button(
            right_frame,
            text="Finalizar Venta",
            command=self.finalizar_venta,
            style="Accent.TButton"
        ).pack(pady=10)
        
        self.cargar_sabores_venta()

    def cargar_sabores_venta(self):
        self.lista_sabores.delete(0, tk.END)
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nombre, precio FROM sabores WHERE stock > 0 ORDER BY nombre")
                for sabor in cursor.fetchall():
                    self.lista_sabores.insert(tk.END, f"{sabor[1]} - ${sabor[2]:.2f}")
                    self.lista_sabores.sabores_data = cursor.fetchall()  # Almacena datos adicionales
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar sabores: {str(e)}")
            finally:
                conn.close()

    def agregar_a_venta(self):
        seleccion = self.lista_sabores.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un sabor primero")
            return
        
        index = seleccion[0]
        sabor_info = self.lista_sabores.get(index).split(" - ")
        nombre = sabor_info[0]
        precio = float(sabor_info[1].replace("$", ""))
        
        self.tree_venta.insert("", "end", values=(nombre, f"{precio:.2f}"))
        self.total_venta.set(self.total_venta.get() + precio)

    def finalizar_venta(self):
        if not self.tree_venta.get_children():
            messagebox.showwarning("Advertencia", "No hay items en la venta")
            return
        
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Registrar venta
                total = self.total_venta.get()
                cursor.execute("INSERT INTO ventas (total) VALUES (%s)", (total,))
                venta_id = cursor.lastrowid
                
                # Registrar detalles
                for item in self.tree_venta.get_children():
                    sabor_nombre = self.tree_venta.item(item)["values"][0]
                    precio = float(self.tree_venta.item(item)["values"][1])
                    
                    cursor.execute("SELECT id FROM sabores WHERE nombre = %s", (sabor_nombre,))
                    sabor_id = cursor.fetchone()[0]
                    
                    cursor.execute(
                        "INSERT INTO detalle_venta (venta_id, sabor_id, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
                        (venta_id, sabor_id, 1, precio)
                    )
                    
                    # Actualizar stock
                    cursor.execute("UPDATE sabores SET stock = stock - 1 WHERE id = %s", (sabor_id,))
                
                conn.commit()
                messagebox.showinfo("Éxito", f"Venta registrada! Total: ${total:.2f}")
                
                # Limpiar venta actual
                for item in self.tree_venta.get_children():
                    self.tree_venta.delete(item)
                self.total_venta.set(0.0)
                
                # Actualizar listas
                self.cargar_sabores_venta()
                self.actualizar_lista_sabores()
                
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo completar la venta: {str(e)}")
            finally:
                conn.close()

    # --- PESTAÑA REPORTES ---
    def setup_reportes_tab(self):
        # Frame principal
        main_frame = ttk.Frame(self.tab_reportes)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview para reportes
        self.tree_reportes = ttk.Treeview(
            main_frame,
            columns=("id", "fecha", "total"),
            show="headings",
            height=15
        )
        
        # Configurar columnas
        self.tree_reportes.heading("id", text="ID Venta")
        self.tree_reportes.heading("fecha", text="Fecha y Hora")
        self.tree_reportes.heading("total", text="Total ($)")
        
        self.tree_reportes.column("id", width=80, anchor="center")
        self.tree_reportes.column("fecha", width=200)
        self.tree_reportes.column("total", width=100, anchor="e")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree_reportes.yview)
        self.tree_reportes.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_reportes.pack(fill="both", expand=True)
        
        # Botón Actualizar
        ttk.Button(
            main_frame,
            text="Actualizar Reportes",
            command=self.actualizar_reportes
        ).pack(pady=10)
        
        self.actualizar_reportes()

    def actualizar_reportes(self):
        for item in self.tree_reportes.get_children():
            self.tree_reportes.delete(item)
        
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT v.id, v.fecha, v.total, 
                           GROUP_CONCAT(s.nombre SEPARATOR ', ') AS sabores
                    FROM ventas v
                    JOIN detalle_venta dv ON v.id = dv.venta_id
                    JOIN sabores s ON dv.sabor_id = s.id
                    GROUP BY v.id
                    ORDER BY v.fecha DESC
                """)
                
                for venta in cursor.fetchall():
                    self.tree_reportes.insert("", "end", values=(
                        venta["id"],
                        venta["fecha"].strftime("%Y-%m-%d %H:%M:%S"),
                        f"{venta['total']:.2f}"
                    ))
                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar reportes: {str(e)}")
            finally:
                conn.close()

# --- EJECUCIÓN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = HeladeriaApp(root)
    root.mainloop()
