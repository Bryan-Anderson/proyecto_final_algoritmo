import sqlite3
# Conectar a la base de datos (si no existe, la creará)
conn = sqlite3.connect('tienda.db')
cursor = conn.cursor()

# Crear la tabla 'inventario' si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventario (
        codigo INTEGER PRIMARY KEY,
        nombre TEXT,
        existencia INTEGER,
        proveedor TEXT,
        precio REAL
    )
''')

# Insertar tres registros en la tabla 'inventario'
cursor.execute("INSERT INTO inventario (nombre, existencia, proveedor, precio) VALUES (?, ?, ?, ?)",
               ('Producto 1', 10, 'Proveedor A', 20.50))
cursor.execute("INSERT INTO inventario (nombre, existencia, proveedor, precio) VALUES (?, ?, ?, ?)",
               ('Producto 2', 15, 'Proveedor B', 15.75))
cursor.execute("INSERT INTO inventario (nombre, existencia, proveedor, precio) VALUES (?, ?, ?, ?)",
               ('Producto 3', 20, 'Proveedor C', 10.00))

# Crear la tabla 'clientes' si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        codigo INTEGER PRIMARY KEY,
        nombre TEXT,
        direccion TEXT
    )
''')

cursor.execute("INSERT INTO clientes (nombre, direccion) VALUES (?, ?)",
               ('Cliente 1', 'Calle 123, Ciudad A'))
cursor.execute("INSERT INTO clientes (nombre, direccion) VALUES (?, ?)",
               ('Cliente 2', 'Av. Principal 456, Ciudad B'))
cursor.execute("INSERT INTO clientes (nombre, direccion) VALUES (?, ?)",
               ('Cliente 3', 'Carrera 789, Ciudad C'))


# Crear la tabla 'ventas' si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY,
        nombre_producto TEXT,
        nombre_cliente TEXT,
        cantidad INTEGER,
        total REAL
    )
''')

# Insertar tres registros en la tabla 'ventas'
cursor.execute("INSERT INTO ventas (nombre_producto, nombre_cliente, cantidad, total) VALUES (?, ?, ?, ?)",
               ('Producto 1', 'Cliente 1', 2, 41.00))
cursor.execute("INSERT INTO ventas (nombre_producto, nombre_cliente, cantidad, total) VALUES (?, ?, ?, ?)",
               ('Producto 2', 'Cliente 2', 3, 47.25))
cursor.execute("INSERT INTO ventas (nombre_producto, nombre_cliente, cantidad, total) VALUES (?, ?, ?, ?)",
               ('Producto 3', 'Cliente 3', 1, 10.00))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

