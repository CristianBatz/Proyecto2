class CodigoDuplicadoError(Exception):
    pass


class RegistroNoExisteError(Exception):
    pass

class Categorias:
    def __init__(self, id_categoria, nombre):
        self.id_categoria = id_categoria
        self.nombre = nombre

class ManipulacionCategorias:
    def __init__(self, categorias):
        self.categoria = {}

    def agregar_categoria(self):
        idc= int(input("Ingrese el id del categoria: "))
        nombre =input("Ingrese el nombre del categoria: ")
        self.categoria[idc] = Categorias(idc,nombre)
        print("Categorias agregada exitosamente")


class Productos:
    def __init__(self, id_producto, nombre, id_categoria, precio, stock, fecha_caducidad=None):
        if not id_producto.strip():
            raise ValueError("El ID del producto no puede quedar vacío.")
        if not nombre.strip():
            raise ValueError("El nombre no puede quedar vacío.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.id_producto = id_producto
        self.nombre = nombre
        self.id_categoria = id_categoria
        self.precio = precio
        self.stock = stock
        self.fecha_caducidad = fecha_caducidad

    def actualizar_precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.precio = nuevo_precio

    def actualizar_stock(self, nuevo_stock):
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.stock = nuevo_stock

    def __str__(self):
        return f"[{self.id_producto}] {self.nombre} | Cat: {self.id_categoria} | Precio: Q{self.precio:.2f} | Stock: {self.stock}"

class Clientes:
    def __init__(self, nit, nombre, telefono, direccion, correo):
        self.nit = nit
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo


class Empleados:
    def __init__(self, id_empleado, nombre, telefono, direccion, correo):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo

class ManipulacionEmpleados:
    def __init__(self):
        self.empleado = {}


class Proveedores:
    def __init__(self, id_proveedor, nombre, empresa, nit, telefono, direccion, correo):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.empresa = empresa
        self.nit = nit
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo

class ManipulacionProveedores:
    def __init__(self):
        self.proveedores: {}

class Ventas:
    def __init__(self, id_venta, fecha, id_cliente, id_empleado):
        self.id_venta = id_venta
        self.fecha = fecha
        self.id_cliente = id_cliente
        self.id_empleado = id_empleado
        self.detalles = []
        self.total = 0

    def agregar_detalle(self, detalle):
        self.detalles.append(detalle)
        self.total += detalle.subtotal

class ManipulacionInventario:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, producto):
        if producto.id_producto in self.productos:
            raise CodigoDuplicadoError("El ID del producto ya existe.")
        idp = input("Ingrese el id del producto: ")
        nombre = input("Ingrese el nombre del producto: ")
        precio = input("Ingrese el precio del producto: ")
        idc = input("Ingrese el id del categoria del producto: ")
        if idc not in self.productos:
            print("Error: La categoría no existe. Agrega primero la categoría.")
        else:
            stock = input("Ingrese el stock del producto: ")
            fecha_caducidad = input("Ingrese la fecha de caducidad: ")
            self.productos[producto.id_producto] = producto(idp, nombre, precio, idc , stock, fecha_caducidad)


    def eliminar_producto(self, id_producto):
        if id_producto not in self.productos:
            raise RegistroNoExisteError("No se encontró el producto.")
        del self.productos[id_producto]

    def actualizar_producto(self, id_producto, nuevo_precio=None, nuevo_stock=None):
        if id_producto not in self.productos:
            raise RegistroNoExisteError("No se encontró el producto.")
        producto = self.productos[id_producto]
        if nuevo_precio is not None:
            producto.actualizar_precio(nuevo_precio)
        if nuevo_stock is not None:
            producto.actualizar_stock(nuevo_stock)

    def obtener_lista(self):
        return list(self.productos.values())

class ManipulacionVentas:
    def __init__(self, inventario: ManipulacionInventario):
        self.inventario = inventario
        self.historial = []

    def vender(self, codigo: str, cantidad: int):
        if codigo not in self.inventario.productos:
            raise RegistroNoExisteError("No se encontró el producto.")
        producto = self.inventario.productos[codigo]
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}")

        producto.stock -= cantidad
        total = cantidad * producto.precio
        self.historial.append((producto.id_producto, producto.nombre, cantidad, total))
        print(f"Venta registrada correctamente. Total: Q{total:.2f}")

    def mostrar_historial(self):
        if not self.historial:
            print("No hay ventas registradas.")
            return

        print("\nHISTORIAL DE VENTAS:")
        total_general = 0
        for codigo, nombre, cantidad, total in self.historial:
            print(f"[{codigo}] {nombre} - {cantidad} unidades - Total: Q{total:.2f}")
            total_general += total
        print(f"\n Total acumulado de ventas: Q{total_general:.2f}")

    def filtrar_por_codigo(self, codigo: str):
        ventas_filtradas = [v for v in self.historial if v[0] == codigo]
        if not ventas_filtradas:
            print("No hay ventas para ese producto.")
            return
        for _, nombre, cantidad, total in ventas_filtradas:
            print(f"{nombre} - {cantidad} unidades - Q{total:.2f}")

class DetallesVentas:
    def __init__(self, id_detalle, id_venta, id_producto, cantidad, precio, subtotal):
        self.id_detalle = id_detalle
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio = precio
        self.subtotal = subtotal


class Compras:
    def __init__(self, id_compra, fecha, id_proveedor, id_empleado):
        self.id_compra = id_compra
        self.fecha = fecha
        self.id_proveedor = id_proveedor
        self.id_empleado = id_empleado
        self.detalles = []
        self.total = 0

    def agregar_detalle(self, detalle):
        self.detalles.append(detalle)
        self.total += detalle.subtotal


class DetallesCompras:
    def __init__(self, id_detalle, id_compra, id_producto, cantidad, precio_compra, subtotal):
        self.id_detalle = id_detalle
        self.id_compra = id_compra
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.subtotal = subtotal

class Buscar:
    def buscar_valor(self, lista, criterio, valor):
        resultados = []
        valor = valor.lower()
        for item in lista:
            if criterio == "id_producto" and item.id_producto.lower() == valor:
                resultados.append(item)
            elif criterio == "nombre" and valor in item.nombre.lower():
                resultados.append(item)
            elif criterio == "categoria" and valor in item.id_categoria.lower():
                resultados.append(item)
        return resultados


class Ordenamiento:
    def quick_sort(self, lista, clave):
        if len(lista) <= 1:
            return lista
        pivote = lista[0]

        if clave == "id_producto":
            menores = [x for x in lista[1:] if x.id_producto < pivote.id_producto]
            iguales = [x for x in lista[1:] if x.id_producto == pivote.id_producto]
            mayores = [x for x in lista[1:] if x.id_producto > pivote.id_producto]

        elif clave == "nombre":
            menores = [x for x in lista[1:] if x.nombre < pivote.nombre]
            iguales = [x for x in lista[1:] if x.nombre == pivote.nombre]
            mayores = [x for x in lista[1:] if x.nombre > pivote.nombre]

        elif clave == "precio":
            menores = [x for x in lista[1:] if x.precio < pivote.precio]
            iguales = [x for x in lista[1:] if x.precio == pivote.precio]
            mayores = [x for x in lista[1:] if x.precio > pivote.precio]

        else:
            raise ValueError("Criterio inválido.")

        return self.quick_sort(menores, clave) + [pivote] + iguales + self.quick_sort(mayores, clave)

class Menu:
    def menu(self):
        print("=== Gestion de supermercado")
        print("1. Agregar un producto")
        print("2. Buscar un producto")
        print("3. Mostrar inventario")
        print("4. Eliminar un producto")
        print("5. Agregar una categoria")
        print("6. Eliminar un categoria")
        print("7. Agregar empleados")
        print("8. Agregar proveedores")
        print("9. Registrar venta")
        print("10. Registrar compra")
        print("11. Salir")