class CodigoDuplicadoError(Exception):
    pass


class RegistroNoExisteError(Exception):
    pass

class Categorias:
    def __init__(self, id_categoria, nombre):
        self.id_categoria = id_categoria
        self.nombre = nombre

class ManipulacionCategorias:
    def __init__(self):
        self.categoria = {}

    def agregar_categoria(self):
        idc= int(input("Ingrese el id del categoria: "))
        nombre =input("Ingrese el nombre del categoria: ")
        self.categoria[idc] = Categorias(idc,nombre)
        print("Categorias agregada exitosamente")

    def mostrar_categorias(self):
        if not self.categoria:
            print("No hay categorias registradas.")
        else:
            for c in self.categoria.values():
                print(f"categoria: {c.id_categoria}, nombre: {c.nombre}")

    def eliminar_categoria(self):
        if idc not in self.categoria:
            raise RegistroNoExisteError("No se encontró el producto.")
        if idc in self.categoria:
            del self.categoria[idc]
            print("Categoria eliminada correctamente.")
        else:
            print("No hay categorias registradas.")



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

class ManipulacionInventario:
    def __init__(self):
        self.productos = {}
        self.contador_id = 1

    def generar_id(self):
        nuevo_id = f"P{self.contador_id:03d}"
        self.contador_id += 1
        return nuevo_id

    def agregar_producto(self, producto):
        if producto.id_producto in self.productos:
            raise CodigoDuplicadoError("El ID del producto ya existe.")
        idp = self.generar_id()
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

class Clientes:
    def __init__(self, nit, nombre, telefono, direccion, correo):
        self.nit = nit
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo

class ManipulacionClientes:
    def __init__(self):
        self.clientes = {}

    def agregar_cliente(self):
        nit = input("Ingrese el NIT del cliente: ")
        nombre = input("Ingrese el nombre del cliente: ")
        telefono = input("Ingrese el teléfono del cliente: ")
        direccion = input("Ingrese la dirección del cliente: ")
        correo = input("Ingrese el correo del cliente: ")
        if nit in self.clientes:
            raise CodigoDuplicadoError("El cliente con este NIT ya existe.")
        self.clientes[nit] = Clientes(nit, nombre, telefono, direccion, correo)
        print("Cliente agregado exitosamente.")

    def eliminar_cliente(self, nit):
        if nit not in self.clientes:
            raise RegistroNoExisteError("No se encontró el cliente.")
        del self.clientes[nit]
        print("Cliente eliminado exitosamente.")

    def mostrar_clientes(self):
        if not self.clientes:
            print("No hay clientes registrados.")
        else:
            for c in self.clientes.values():
                print(f"NIT: {c.nit} | Nombre: {c.nombre} | Tel: {c.telefono}")


class Empleados:
    def __init__(self, id_empleado, nombre, telefono, direccion, correo):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo

class ManipulacionEmpleados:
    def __init__(self):
        self.empleados = {}

    def agregar_empleado(self):
        ide = input("Ingrese el ID del empleado: ")
        nombre = input("Ingrese el nombre del empleado: ")
        telefono = input("Ingrese el teléfono del empleado: ")
        direccion = input("Ingrese la dirección del empleado: ")
        correo = input("Ingrese el correo del empleado: ")
        if ide in self.empleados:
            raise CodigoDuplicadoError("El empleado con este ID ya existe.")
        self.empleados[ide] = Empleados(ide, nombre, telefono, direccion, correo)
        print("Empleado agregado exitosamente.")

    def eliminar_empleado(self, ide):
        if ide not in self.empleados:
            raise RegistroNoExisteError("No se encontró el empleado.")
        del self.empleados[ide]
        print("Empleado eliminado exitosamente.")

    def mostrar_empleados(self):
        if not self.empleados:
            print("No hay empleados registrados.")
        else:
            for e in self.empleados.values():
                print(f"ID: {e.id_empleado} | Nombre: {e.nombre} | Tel: {e.telefono}")


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
        self.proveedores = {}

    def agregar_proveedor(self):
        id_proveedor = input("Ingrese el ID del proveedor: ")
        nombre = input("Ingrese el nombre del proveedor: ")
        empresa = input("Ingrese la empresa del proveedor: ")
        nit = input("Ingrese el NIT del proveedor: ")
        telefono = input("Ingrese el teléfono del proveedor: ")
        direccion = input("Ingrese la dirección del proveedor: ")
        correo = input("Ingrese el correo del proveedor: ")
        if id_proveedor in self.proveedores:
            raise CodigoDuplicadoError("El proveedor con este ID ya existe.")
        self.proveedores[id_proveedor] = Proveedores(id_proveedor, nombre, empresa, nit, telefono, direccion, correo)
        print("Proveedor agregado exitosamente.")

    def eliminar_proveedor(self, id_proveedor):
        if id_proveedor not in self.proveedores:
            raise RegistroNoExisteError("No se encontró el proveedor.")
        del self.proveedores[id_proveedor]
        print("Proveedor eliminado exitosamente.")

    def mostrar_proveedores(self):
        if not self.proveedores:
            print("No hay proveedores registrados.")
        else:
            for p in self.proveedores.values():
                print(f"ID: {p.id_proveedor} | Nombre: {p.nombre} | Empresa: {p.empresa}")

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

    def calcular_subtotal(self):
        self.subtotal = self.cantidad * self.precio

    def mostrar_detalle(self):
        return f"Detalle {self.id_detalle}: Producto {self.id_producto} | Cant: {self.cantidad} | Precio: Q{self.precio:.2f} | Subtotal: Q{self.subtotal:.2f}"

    def actualizar_cantidad(self, nueva_cantidad):
        if nueva_cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        self.cantidad = nueva_cantidad
        self.calcular_subtotal()

    def actualizar_precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.precio = nuevo_precio
        self.calcular_subtotal()


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

class ManipulacionCompras:
    def __init__(self):
        self.historial = []

    def registrar_compra(self):
        id_compra = input("Ingrese el ID de la compra: ")
        fecha = input("Ingrese la fecha: ")
        id_proveedor = input("Ingrese el ID del proveedor: ")
        id_empleado = input("Ingrese el ID del empleado que registró la compra: ")
        compra = Compras(id_compra, fecha, id_proveedor, id_empleado)

        while True:
            id_producto = input("Ingrese el ID del producto (o '0' para terminar): ")
            if id_producto == "0":
                break
            cantidad = int(input("Ingrese la cantidad: "))
            precio = float(input("Ingrese el precio de compra: "))
            subtotal = cantidad * precio
            detalle = DetallesCompras(len(compra.detalles)+1, id_compra, id_producto, cantidad, precio, subtotal)
            compra.agregar_detalle(detalle)

        self.historial.append(compra)
        print(f"Compra registrada exitosamente. Total: Q{compra.total:.2f}")

    def mostrar_historial(self):
        if not self.historial:
            print("No hay compras registradas.")
        else:
            for c in self.historial:
                print(f"Compra {c.id_compra} | Proveedor: {c.id_proveedor} | Total: Q{c.total:.2f}")


class DetallesCompras:
    def __init__(self, id_detalle, id_compra, id_producto, cantidad, precio_compra, subtotal):
        self.id_detalle = id_detalle
        self.id_compra = id_compra
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.subtotal = subtotal

    def calcular_subtotal(self):
        self.subtotal = self.cantidad * self.precio_compra

    def mostrar_detalle(self):
        return f"Detalle {self.id_detalle}: Producto {self.id_producto} | Cant: {self.cantidad} | Precio compra: Q{self.precio_compra:.2f} | Subtotal: Q{self.subtotal:.2f}"

    def actualizar_cantidad(self, nueva_cantidad):
        if nueva_cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        self.cantidad = nueva_cantidad
        self.calcular_subtotal()

    def actualizar_precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.precio_compra = nuevo_precio
        self.calcular_subtotal()

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
        print("\n=== SISTEMA DE GESTIÓN DE SUPERMERCADO ===")
        print("1.  Agregar producto")
        print("2.  Mostrar inventario")
        print("3.  Eliminar producto")
        print("4.  Actualizar producto")
        print("5.  Buscar producto")
        print("6.  Agregar categoría")
        print("7.  Mostrar categorías")
        print("8.  Eliminar categoría")
        print("9.  Agregar empleado")
        print("10. Mostrar empleados")
        print("11. Eliminar empleado")
        print("12. Agregar proveedor")
        print("13. Mostrar proveedores")
        print("14. Eliminar proveedor")
        print("15. Agregar cliente")
        print("16. Mostrar clientes")
        print("17. Eliminar cliente")
        print("18. Registrar venta")
        print("19. Mostrar historial de ventas")
        print("20. Filtrar ventas por producto")
        print("21. Registrar compra")
        print("22. Mostrar historial de compras")
        print("23. Salir")

manipulacion_inventario = ManipulacionInventario()
manipulacion_categorias = ManipulacionCategorias()
manipulacion_clientes = ManipulacionClientes()
manipulacion_empleados = ManipulacionEmpleados()
manipulacion_proveedores = ManipulacionProveedores()
manipulacion_ventas = ManipulacionVentas(manipulacion_inventario)
manipulacion_compras = ManipulacionCompras()
buscador = Buscar()
ordenamiento = Ordenamiento()
menu = Menu()
opcion = 0
while opcion != 23:
    menu.menu()
    try:
        opcion = int(input("Seleccione una opcion: "))
    except ValueError:
        print("Opcion no valida")
        continue

    match opcion:
        case 1:
            try:
                nombre = input("Ingrese el nombre: ")
                idc = input("Ingrese el ID de la categoría: ")
                precio = float(input("Ingrese el precio: "))
                stock = int(input("Ingrese el stock: "))
                fecha = input("Ingrese la fecha de caducidad: ")
                producto = Productos(nombre, idc, precio, stock, fecha)
                manipulacion_inventario.agregar_producto(producto)
                print("Producto agregado correctamente.")
            except Exception as e:
                print(f"Error: {e}")

        case 2:
            lista = manipulacion_inventario.obtener_lista()
            if not lista:
                print("No hay productos registrados.")
            else:
                for p in lista:
                    print(p)

        case 3:
            idp = input("Ingrese el ID del producto a eliminar: ")
            try:
                manipulacion_inventario.eliminar_producto(idp)
                print("Producto eliminado correctamente.")
            except Exception as e:
                print(f"Error: {e}")

        case 4:
            idp = input("Ingrese el ID del producto a actualizar: ")
            nuevo_precio = float(input("Nuevo precio (deje vacío para no cambiar): ") or -1)
            nuevo_stock = int(input("Nuevo stock (deje vacío para no cambiar): ") or -1)
            try:
                manipulacion_inventario.actualizar_producto(
                    idp,
                    nuevo_precio if nuevo_precio >= 0 else None,
                    nuevo_stock if nuevo_stock >= 0 else None
                )
                print("Producto actualizado correctamente.")
            except Exception as e:
                print(f"Error: {e}")

        case 5:
            criterio = input("Buscar por (id_producto/nombre/categoria): ")
            valor = input("Valor a buscar: ")
            lista = manipulacion_inventario.obtener_lista()
            resultados = buscador.buscar_valor(lista, criterio, valor)
            if resultados:
                for r in resultados:
                    print(r)
            else:
                print("No se encontraron resultados.")

        case 6:
            manipulacion_categorias.agregar_categoria()

        case 7:
            if not manipulacion_categorias.categoria:
                print("No hay categorías registradas.")
            else:
                for c in manipulacion_categorias.categoria.values():
                    print(f"ID: {c.id_categoria} | Nombre: {c.nombre}")

        case 8:
            idc = int(input("Ingrese el ID de la categoría a eliminar: "))
            manipulacion_categorias.eliminar_categoria()


        case 9:
            try:
                manipulacion_empleados.agregar_empleado()
            except Exception as e:
                print(f"Error: {e}")

