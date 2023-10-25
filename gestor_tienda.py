import sqlite3
import argparse
from email.mime.text import MIMEText
import smtplib
import os
from tabulate import tabulate




def listar_tabla_inventario():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM inventario")
    datos = cursor.fetchall()

    columnas = [descripcion[0] for descripcion in cursor.description]

    print(tabulate(datos, headers=columnas, tablefmt="fancy_grid"))

    conn.close()

def agregar_producto_interactivo():
    codigo = int(input("Código del producto: "))
    nombre = input("Nombre del producto: ")
    existencia = int(input("Existencia del producto: "))
    proveedor = input("Proveedor del producto: ")
    precio = float(input("Precio del producto: "))

    
    conexion = sqlite3.connect('tienda.db')
    cursor = conexion.cursor()
    
   
    cursor.execute('''
        INSERT INTO inventario (codigo, nombre, existencia, proveedor, precio)
        VALUES (?, ?, ?, ?, ?)
    ''', (codigo, nombre, existencia, proveedor, precio))
    
   
    conexion.commit()
    conexion.close()



def editar_producto(codigo, nombre, existencia, proveedor, precio):
    conexion = sqlite3.connect('tienda.db')
    cursor = conexion.cursor()

    cursor.execute('''
        UPDATE inventario
        SET nombre=?, existencia=?, proveedor=?, precio=?
        WHERE codigo=?
    ''', (nombre, existencia, proveedor, precio, codigo))

    conexion.commit()
    conexion.close()

def eliminar_producto(nombre):
    conexion = sqlite3.connect('tienda.db')
    cursor = conexion.cursor()

    cursor.execute('''
        DELETE FROM inventario
        WHERE nombre=?
    ''', (nombre,))

    conexion.commit()
    conexion.close()











def listar_tabla_clientes():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM clientes")
    datos = cursor.fetchall()

    columnas = [descripcion[0] for descripcion in cursor.description]

    print(tabulate(datos, headers=columnas, tablefmt="fancy_grid"))

    conn.close()



def agregar_clientes_interactivo():
    codigo = int(input("Código del cliente: "))
    nombre = input("Nombre del cliente: ")
    direccion = (input("Escriba la direccion del cliete: "))
    

    
    conexion = sqlite3.connect('tienda.db')
    cursor = conexion.cursor()
    
    
    cursor.execute('''
        INSERT INTO clientes (codigo, nombre, direccion)
        VALUES (?, ?, ?)
    ''', (codigo, nombre, direccion))
    
    
    conexion.commit()
    conexion.close()




def editar_clientes(codigo, nombre, direccion):
    conexion = sqlite3.connect('tienda.db')
    cursor = conexion.cursor()

    cursor.execute('''
        UPDATE clientes
        SET nombre=?, direccion=?
        WHERE codigo=?
    ''', (nombre, direccion, codigo))

    conexion.commit()
    conexion.close()



def eliminar_clientes(nombre):
    conexion = sqlite3.connect('tienda.db')
    cursor = conexion.cursor()

    cursor.execute('''
        DELETE FROM clientes
        WHERE nombre=?
    ''', (nombre,))

    conexion.commit()
    conexion.close()







def listar_tabla_ventas():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM ventas")
    datos = cursor.fetchall()

    columnas = [descripcion[0] for descripcion in cursor.description]

    print(tabulate(datos, headers=columnas, tablefmt="fancy_grid"))

    conn.close()






def realizar_venta():
    
    id_producto = int(input("Ingrese el ID del producto: "))
    nombre_producto = input("Ingrese el nombre del producto: ")
    nombre_cliente = input("Ingrese el nombre del cliente: ")
    cantidad = int(input("Ingrese la cantidad: "))
    total = float(input("Ingrese el total: "))

    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    cursor.execute("SELECT existencia FROM inventario WHERE codigo=?", (id_producto,))
    existencia = cursor.fetchone()
    if existencia and cantidad <= existencia[0]:
        cursor.execute("UPDATE inventario SET existencia = existencia - ? WHERE codigo=?", (cantidad, id_producto))
        cursor.execute("INSERT INTO ventas (nombre_producto, nombre_cliente, cantidad, total) VALUES (?, ?, ?, ?)",
                       (nombre_producto, nombre_cliente, cantidad, total))
        conn.commit()
        conn.close()
        print(f"Venta realizada con éxito. Total: {total}")
    else:
        print(f"No hay suficiente existencia de {nombre_producto} o el producto no existe.")







def anular_venta():
    id_venta = int(input("Ingrese el ID de la venta que desea anular: "))

    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ventas WHERE id=?", (id_venta,))
    venta = cursor.fetchone()

    if venta:
        id_producto = venta[1]  
        cantidad = venta[3]     

        cursor.execute("UPDATE inventario SET existencia = existencia + ? WHERE codigo=?", (cantidad, id_producto))
        cursor.execute("DELETE FROM ventas WHERE id=?", (id_venta,))
        
        conn.commit()
        conn.close()
        print(f"Venta anulada con éxito.")
    else:
        print(f"No se encontró ninguna venta con el ID {id_venta}.")






def generar_reporte_cliente():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT clientes.nombre, clientes.direccion, SUM(ventas.total)
        FROM clientes
        JOIN ventas ON clientes.nombre = ventas.nombre_cliente
        GROUP BY clientes.nombre, clientes.direccion
    ''')

    reporte = cursor.fetchall()

    conn.close()

    return reporte

def generar_reporte_producto():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT inventario.nombre, SUM(ventas.cantidad), SUM(ventas.total)
        FROM inventario
        JOIN ventas ON inventario.nombre = ventas.nombre_producto
        GROUP BY inventario.nombre
    ''')

    reporte = cursor.fetchall()

    conn.close()

    return reporte

def enviar_reporte(asunto, mensaje, destinatario):
    contrasena = os.getenv('GOOGLE_APP_PASS')
    usuario = os.getenv("GOOGLE_APP_EMAIL")

    msg = MIMEText(mensaje, 'plain', 'utf-8')
    msg['Subject'] = asunto
    msg['From'] = "reportes"
    msg['To'] = destinatario

    try:
        smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_object.starttls()
        smtp_object.login(usuario, contrasena)
        smtp_object.sendmail(msg['From'], msg['To'], msg.as_string())
        print("Correo enviado exitosamente")
        smtp_object.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def generar_y_enviar_reporte(por_cliente, por_productos):
    if por_cliente:
        reporte = generar_reporte_cliente()
        asunto = "Reporte por Cliente"
        mensaje = tabulate(reporte, headers=["Nombre", "Dirección", "Total Comprado"], tablefmt="plain")
    elif por_productos:
        reporte = generar_reporte_producto()
        asunto = "Reporte por Producto"
        mensaje = tabulate(reporte, headers=["Nombre", "Cantidad Vendida", "Total Ventas"], tablefmt="plain")
    else:
        print("Debes seleccionar al menos una opción (--por_cliente o --por_productos).")
        return

    destinatario = "tu_correo@gmail.com"  
    enviar_reporte(asunto, mensaje, destinatario)
















parser = argparse.ArgumentParser(description='programa administrar tiendas')

subparsers = parser.add_subparsers(title='Operaciones', dest='subcomando')

tabla_inventario_parser = subparsers.add_parser('inventario', help='se refiere a tabla inventario')
tabla_inventario_parser.add_argument('--listar', action='store_true', help='Nos muestra la tabla de inventario')
tabla_inventario_parser.add_argument('--agregar', action='store_true', help='Agrega un producto a la tabla de inventario')
tabla_inventario_parser.add_argument('--editar', action='store_true', help='Edita un producto en la tabla de inventario')
tabla_inventario_parser.add_argument('--eliminar', action='store_true', help='Elimina un producto de la tabla de inventario')



tabla_clientes_parser = subparsers.add_parser('clientes', help='se refiere a tabla clientes')
tabla_clientes_parser.add_argument('--listar_c', action='store_true', help='Nos muestra la tabla de clientes')
tabla_clientes_parser.add_argument('--agregar_c', action='store_true', help='Agrega un producto a la tabla de clientes')
tabla_clientes_parser.add_argument('--editar_c', action='store_true', help='Edita un producto en la tabla de clientes')
tabla_clientes_parser.add_argument('--eliminar_c', action='store_true', help='Elimina un producto de la tabla de clientes')



tabla_ventas_parser = subparsers.add_parser('ventas', help='se refiere a tabla ventas')
tabla_ventas_parser.add_argument('--listar_v', action='store_true', help='Nos muestra la tabla de ventas')
tabla_ventas_parser.add_argument('--crear_v', action='store_true', help='Agrega un producto a la tabla de ventas')
tabla_ventas_parser.add_argument('--anular_v', action='store_true', help='Edita un producto en la tabla de clientes')



reportes_parser = subparsers.add_parser('reportes', help='comado para generar reportes')
reportes_parser.add_argument('--por_cliente', action='store_true', help='genera reportes por cliente')
reportes_parser.add_argument('--por_productos', action='store_true', help='genera reportes por producto')



args = parser.parse_args()

if args.subcomando == 'inventario':
    if args.listar:
        listar_tabla_inventario()

    if args.agregar:
        agregar_producto_interactivo()
    
    if args.editar:
        codigo = int(input("Código del producto a editar: "))
        nombre = input("Nuevo nombre del producto: ")
        existencia = int(input("Nueva existencia del producto: "))
        proveedor = input("Nuevo proveedor del producto: ")
        precio = float(input("Nuevo precio del producto: "))
        editar_producto(codigo, nombre, existencia, proveedor, precio)

    if args.eliminar:
        nombre_producto = input("Nombre del producto a eliminar: ")
        eliminar_producto(nombre_producto)





if args.subcomando == 'clientes':

    if args.listar_c:
        listar_tabla_clientes()

    if args.agregar_c:
        agregar_clientes_interactivo()

    if args.editar_c:
        codigo = int(input("Código del cliente: "))
        nombre = input("Nombre del cliente: ")
        direccion = (input("Escriba la direccion del cliete: "))
        editar_clientes(codigo, nombre, direccion)

    if args.eliminar_c:
        nombre_cliente = input("Nombre del cliente a eliminar: ")
        eliminar_clientes(nombre_cliente)








if args.subcomando == 'ventas':

    if args.listar_v:
        listar_tabla_ventas()
    
    if args.crear_v:
      realizar_venta()

    if args.anular_v:
        anular_venta()


if args.command == 'reportes':
    generar_y_enviar_reporte(args.por_cliente, args.por_productos)