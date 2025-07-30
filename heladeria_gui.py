def setup_sabores_tab(self):
    # Marco para el formulario
    form_frame = ttk.Frame(self.tab_sabores)
    form_frame.pack(pady=10, padx=10, fill="x")

    # Campo Nombre
    ttk.Label(form_frame, text="Nombre del sabor:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    self.nombre_sabor = ttk.Entry(form_frame, width=30)
    self.nombre_sabor.grid(row=0, column=1, padx=5, pady=5)

    # Campo Precio
    ttk.Label(form_frame, text="Precio ($):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    self.precio_sabor = ttk.Entry(form_frame, width=10)
    self.precio_sabor.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Campo Stock
    ttk.Label(form_frame, text="Stock inicial:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    self.stock_sabor = ttk.Spinbox(form_frame, from_=0, to=1000, width=8)
    self.stock_sabor.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Botón Guardar
    ttk.Button(
        form_frame,
        text="Guardar Sabor",
        command=self.registrar_sabor,
        style="Accent.TButton"
    ).grid(row=3, columnspan=2, pady=10)

    # Tabla de sabores (Treeview)
    self.tree_sabores = ttk.Treeview(
        self.tab_sabores,
        columns=("id", "nombre", "precio", "stock"),
        show="headings",
        height=10
    )
    self.tree_sabores.heading("id", text="ID")
    self.tree_sabores.heading("nombre", text="Nombre")
    self.tree_sabores.heading("precio", text="Precio ($)")
    self.tree_sabores.heading("stock", text="Stock")
    self.tree_sabores.pack(pady=10, padx=10, fill="both", expand=True)
    self.actualizar_lista_sabores()
