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
        self.cargar_categorias()

    def cargar_categorias(self):
        try:
            with open("categorias.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea:
                        id_categoria,nombre = linea.split(":")
                        id_categoria = int(id_categoria)
                        self.categoria[id_categoria] = Categorias(id_categoria, nombre)
            print("categoria importados desde categorias.txt")
        except FileNotFoundError:
            print("No existe el archivo categorias.txt, se creará uno nuevo al guardar.")

    def guardar_categoria(self):
        with open("categorias.txt", "w", encoding="utf-8") as archivo:
            for id_categoria, datos in self.categoria.items():
                archivo.write(f"{id_categoria}:{datos.nombre}\n")

    def agregar_categoria(self):
        try:
            idc = int(input("Ingrese el ID de la categoría: "))
            nombre = input("Ingrese el nombre de la categoría: ")
            if idc in self.categoria:
                print("Error: Ya existe una categoría con ese ID.")
            else:
                self.categoria[idc] = Categorias(idc, nombre)
                self.guardar_categoria()
                print(f"Categoría '{nombre}' agregada correctamente con ID {idc}.")
        except ValueError:
            print("Error: El ID debe ser un número entero.")

    def mostrar_categorias(self):
        if not self.categoria:
            print("No hay categorias registradas.")
        else:
            for c in self.categoria.values():
                print(f"categoria: {c.id_categoria}, nombre: {c.nombre}")

    def eliminar_categoria(self):
        if not self.categoria:
            print("No hay categorías registradas.")
            return

        try:
            idc = int(input("Ingrese el ID de la categoría a eliminar: "))
            if idc not in self.categoria:
                raise RegistroNoExisteError("No se encontró la categoría.")
            del self.categoria[idc]
            print("Categoría eliminada correctamente.")
        except ValueError:
            print("Error: El ID debe ser un número entero.")
        except RegistroNoExisteError as e:
            print(f"Error: {e}")


class Productos:
    def __init__(self,id_producto, nombre, id_categoria, precio, stock, fecha_caducidad=None):
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
        nuevo_id = f"{self.contador_id}"
        self.contador_id += 1
        return nuevo_id

    def agregar_varios_productos(self, manipulacion_categorias):
        if not manipulacion_categorias.categoria:
            print("No hay categorías registradas. Agrega primero una categoría.")
            return

        print("Lista de categorías disponibles:")
        for c in manipulacion_categorias.categoria.values():
            print(f"ID: {c.id_categoria} | Nombre: {c.nombre}")

        while True:
            nombre = input("\nIngrese el nombre del producto (o '0' para terminar): ").strip()
            if nombre == "0":
                break
            if not nombre:
                print("Error: El nombre no puede quedar vacío.")
                continue

            try:
                id_categoria = int(input("Ingrese el ID de la categoría: "))
                if id_categoria not in manipulacion_categorias.categoria:
                    print("Error: La categoría no existe.")
                    continue

                precio = float(input("Ingrese el precio: "))
                if precio < 0:
                    print("Error: El precio no puede ser negativo.")
                    continue

                stock = int(input("Ingrese el stock: "))
                if stock < 0:
                    print("Error: El stock no puede ser negativo.")
                    continue

                fecha = input("Ingrese la fecha de caducidad: ").strip()

                duplicado = False
                for p in self.productos.values():
                    if p.nombre.lower() == nombre.lower() and p.id_categoria == id_categoria:
                        duplicado = True
                        break
                if duplicado:
                    print("Error: Este producto ya existe en esta categoría.")
                    continue

                id_producto = self.generar_id()
                nuevo_producto = Productos(id_producto, nombre, id_categoria, precio, stock, fecha)
                self.productos[id_producto] = nuevo_producto
                print(f"Producto '{nombre}' agregado correctamente con ID {id_producto}.")

            except ValueError:
                print("Error: Uno de los valores ingresados no tiene el formato correcto.")

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
        self.cargar_clientes()

    def cargar_clientes(self):
        try:
            with open("clientes.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea:
                        nit, nombre,telefono, direccion , correo = linea.split(":")
                        self.clientes[nit] = Clientes(nit, nombre, telefono, direccion, correo)
            print("Clientes importados desde clientes.txt")
        except FileNotFoundError:
            print("No existe el archivo clientes.txt, se creará uno nuevo al guardar.")

    def guardar_clientes(self):
        with open("clientes.txt", "w", encoding="utf-8") as archivo:
            for nit, datos in self.clientes.items():
                archivo.write(f"{nit}:{datos.nombre}:{datos.telefono}:{datos.direccion}:{datos.correo}\n")

    def agregar_cliente(self):
        nit = input("Ingrese el NIT del cliente: ")
        nombre = input("Ingrese el nombre del cliente: ")
        telefono = input("Ingrese el teléfono del cliente: ")
        direccion = input("Ingrese la dirección del cliente: ")
        correo = input("Ingrese el correo del cliente: ")
        if nit in self.clientes:
            raise CodigoDuplicadoError("El cliente con este NIT ya existe.")
        self.clientes[nit] = Clientes(nit, nombre, telefono, direccion, correo)
        self.guardar_clientes()
        print(f"Cliente con NIT {nit} agregado y guardado correctamente.")

    def mostrar_todos(self):
        if self.clientes:
            print("\nLista de clientes:")
            for nit, datos in self.clientes.items():
                print(f"\n nit: {nit}")
                print(f"nombre: {datos.nombre}")
                print(f"telefono: {datos.telefono}")
                print(f"direccion: {datos.direccion}")
                print(f"correo: {datos.correo}")
        else:
            print("No hay clientes registrados.")

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
        self.cargar_empleados()

    def cargar_empleados(self):
        try:
            with open("Empleados.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea:
                        id_empleado,nombre,telefono,direccion,correo = linea.split(":")
                        self.empleados[id_empleado] = Empleados(id_empleado,nombre,telefono,direccion,correo)
            print("Empleados importados desde Empleados.txt")
        except FileNotFoundError:
            print("No existe el archivo Empleados.txt, se creará uno nuevo al guardar.")

    def guardar_empleados(self):
        with open("Empleados.txt", "w", encoding="utf-8") as archivo:
            for id_empleado, datos in self.empleados.items():
                archivo.write(f"{id_empleado}:{datos.nombre}:{datos.telefono}:{datos.direccion}:{datos.correo}\n")

    def agregar_empleado(self):
        ide = input("Ingrese el ID del empleado: ")
        nombre = input("Ingrese el nombre del empleado: ")
        telefono = input("Ingrese el teléfono del empleado: ")
        direccion = input("Ingrese la dirección del empleado: ")
        correo = input("Ingrese el correo del empleado: ")
        if ide in self.empleados:
            raise CodigoDuplicadoError("El empleado con este ID ya existe.")
        self.empleados[ide] = Empleados(ide, nombre, telefono, direccion, correo)
        self.guardar_empleados()
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
        self.cargar_proveedores()

    def cargar_proveedores(self):
        try:
            with open("Proveedores.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea:
                        id_proveedor,nombre,empresa,nit,telefono,direccion,correo = linea.split(":")
                        self.proveedores[id_proveedor] = Proveedores(id_proveedor,nombre,empresa,nit,telefono,direccion,correo)
            print("Proveedores importados desde Proveedores.txt")
        except FileNotFoundError:
            print("No existe el archivo Proveedores.txt, se creará uno nuevo al guardar.")

    def guardar_proveedores(self):
        with open("Proveedores.txt", "w", encoding="utf-8") as archivo:
            for id_proveedor, datos in self.proveedores.items():
                archivo.write(f"{id_proveedor}:{datos.nombre}:{datos.empresa}:{datos.nit}:{datos.telefono}:{datos.direccion}:{datos.correo}\n")

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
        self.guardar_proveedores()
        print(f"Proveedor con ID:{id_proveedor} agregado exitosamente.")

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
                print(f"ID: {p.id_proveedor} | Nombre: {p.nombre} | Empresa: {p.empresa} | Telefono: {p.telefono}")


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

class ManipulacionCompras:
    def __init__(self, inventario: ManipulacionInventario):
        self.inventario = inventario
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
            producto = self.inventario.productos[id_producto]
            subtotal = cantidad * precio
            detalle = DetallesCompras(len(compra.detalles) + 1, id_compra, id_producto, cantidad, precio, subtotal)
            compra.agregar_detalle(detalle)
            producto.stock += cantidad
            self.historial.append((producto.id_producto, producto.nombre, cantidad, subtotal))

        self.historial.append(compra)
        print(f"Compra registrada exitosamente. Total: Q{compra.total:.2f}")

    def mostrar_historial(self):
        if not self.historial:
            print("No hay compras registradas.")
        else:
            for c in self.historial:
                print(f"Compra: {c.id_compra} | Proveedor: {c.id_proveedor} | Total: Q{c.total:.2f}")

class Buscar:
    def buscar_valor(self, lista, criterio, valor):
        resultados = []
        valor = valor.lower()
        for item in lista:
            if criterio == "id" and item.id_producto.lower() == valor:
                resultados.append(item)
            elif criterio == "nombre" and valor in item.nombre.lower():
                resultados.append(item)
            elif criterio == "categoria" and valor == str(item.id_categoria):
                resultados.append(item)
        return resultados


class Ordenamiento:
    def quick_sort(self, lista, clave):
        if len(lista) <= 1:
            return lista
        pivote = lista[0]

        if clave == "id":
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
manipulacion_compras = ManipulacionCompras(manipulacion_inventario)
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

    match int(opcion):
        case 1:
            manipulacion_inventario.agregar_varios_productos(manipulacion_categorias)

        case 2:
            lista = manipulacion_inventario.obtener_lista()
            if not lista:
                print("No hay productos registrados.")
            else:
                for p in lista:
                    print(p)
                criterio = input("Ingrese el criterio a ordenar(id,nombre,precio): ")
                lista_ordenada = ordenamiento.quick_sort(lista,criterio)
                for p1 in lista_ordenada:
                    print(p1)


        case 3:
            idp = input("Ingrese el ID del producto a eliminar: ")
            try:
                manipulacion_inventario.eliminar_producto(idp)
                print("Producto eliminado correctamente.")
            except Exception as e:
                print(f"Error: {e}")

        case 4:
            idp = input("Ingrese el ID del producto a actualizar: ")
            entrada_precio = input("Nuevo precio (deje vacío para no cambiar): ")
            nuevo_precio = float(entrada_precio) if entrada_precio.strip() else None

            entrada_stock = input("Nuevo stock (deje vacío para no cambiar): ")
            nuevo_stock = int(entrada_stock) if entrada_stock.strip() else None
            try:
                manipulacion_inventario.actualizar_producto(idp, nuevo_precio,nuevo_stock )
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
            manipulacion_categorias.eliminar_categoria()

        case 9:
            try:
                manipulacion_empleados.agregar_empleado()
            except Exception as e:
                print(f"Error: {e}")

        case 10:
            manipulacion_empleados.mostrar_empleados()

        case 11:
            ide = input("Ingrese el ID del empleado a eliminar: ")
            try:
                manipulacion_empleados.eliminar_empleado(ide)
            except Exception as e:
                print(f"Error: {e}")

        case 12:
            try:
                manipulacion_proveedores.agregar_proveedor()
            except Exception as e:
                print(f"Error: {e}")

        case 13:
            manipulacion_proveedores.mostrar_proveedores()

        case 14:
            idp = input("Ingrese el ID del proveedor a eliminar: ")
            try:
                manipulacion_proveedores.eliminar_proveedor(idp)
            except Exception as e:
                print(f"Error: {e}")

        case 15:
            try:
                manipulacion_clientes.agregar_cliente()
            except Exception as e:
                print(f"Error: {e}")

        case 16:
            manipulacion_clientes.mostrar_clientes()

        case 17:
            nit = input("Ingrese el NIT del cliente a eliminar: ")
            try:
                manipulacion_clientes.eliminar_cliente(nit)
            except Exception as e:
                print(f"Error: {e}")

        case 18:
            codigo = input("Ingrese el código del producto: ")
            cantidad = int(input("Ingrese la cantidad: "))
            try:
                manipulacion_ventas.vender(codigo, cantidad)
            except Exception as e:
                print(f"Error: {e}")

        case 19:
            manipulacion_ventas.mostrar_historial()

        case 20:
            codigo = input("Ingrese el código del producto: ")
            manipulacion_ventas.filtrar_por_codigo(codigo)

        case 21:
            manipulacion_compras.registrar_compra()

        case 22:
            manipulacion_compras.mostrar_historial()

        case 23:
            print("Saliendo del sistema")

        case _:
            print(" Opción inválida.")
