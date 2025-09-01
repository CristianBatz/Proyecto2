class CodigoDuplicadoError(Exception):
    pass


class RegistroNoExisteError(Exception):
    pass

class Usuario:
    def __init__(self, nombre, password, rol):
        self.nombre = nombre
        self.password = password
        self.rol = rol

class SistemaUsuarios:
    def __init__(self):
        self.usuarios = {}
        self.cargar_usuarios()

    def cargar_usuarios(self):
        try:
            with open("Usuarios.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea:
                        nombre, password, rol = linea.split(":")
                        self.usuarios[nombre] = Usuario(nombre, password, rol)
            print("Usuarios importados desde Usuarios.txt")
        except FileNotFoundError:
            print("No existe el archivo Usuarios.txt, se creará uno nuevo al guardar.")

    def guardar_usuarios(self):
        with open("Usuarios.txt", "w", encoding="utf-8") as archivo:
            for nombre, datos in self.usuarios.items():
                archivo.write(f"{datos.nombre}:{datos.password}:{datos.rol}\n")

    def registrar(self, nombre, password, rol):
        if nombre in self.usuarios:
            raise CodigoDuplicadoError("El usuario ya existe.")
        self.usuarios[nombre] = Usuario(nombre, password, rol)
        self.guardar_usuarios()

    def login(self, nombre, password):
        if nombre not in self.usuarios:
            raise RegistroNoExisteError("El usuario no existe.")
        usuario = self.usuarios[nombre]
        if usuario.password != password:
            raise ValueError("Contraseña incorrecta.")
        return usuario

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
                        id_categoria, nombre = linea.split(":")
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
            try:
                idc = int(input("Ingrese el ID de la categoría: "))
            except ValueError:
                print("Error: El ID debe ser un número entero.")
                return
            nombre = input("Ingrese el nombre de la categoría: ").strip()
            if not nombre:
                raise ValueError("El nombre de la categoría no puede quedar vacío.")
            if idc in self.categoria:
                raise CodigoDuplicadoError(f"Ya existe una categoría con ID {idc}")
            else:
                self.categoria[idc] = Categorias(idc, nombre)
                self.guardar_categoria()
                print(f"Categoría '{nombre}' agregada correctamente con ID {idc}.")
        except ValueError:
            print("Error: El ID debe ser un número entero.")
        except CodigoDuplicadoError as e:
            print(f"Error de duplicado: {e}")

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
            self.guardar_categoria()
            print("Categoría eliminada correctamente.")
        except ValueError:
            print("Error: El ID debe ser un número entero.")
        except RegistroNoExisteError as e:
            print(f"Error: {e}")


class Productos:
    def __init__(self, id_producto, nombre, id_categoria, precio, stock, fecha_caducidad=None):
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
        self.cargar_productos()

    def generar_id(self):
        nuevo_id = self.contador_id
        self.contador_id += 1
        return nuevo_id

    def cargar_productos(self):
        try:
            with open("productos.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea:
                        partes = linea.split(":")
                        if len(partes) == 6:
                            id_producto, nombre, id_categoria, precio, stock, fecha = partes
                        else:
                            id_producto, nombre, id_categoria, precio, stock = partes
                            fecha = None

                        id_producto = int(id_producto)
                        id_categoria = int(id_categoria)
                        precio = float(precio)
                        stock = int(stock)

                        self.productos[id_producto] = Productos(id_producto, nombre, id_categoria, precio, stock, fecha)
                        if id_producto >= self.contador_id:
                            self.contador_id = id_producto + 1

            print("Productos importados desde productos.txt")
        except FileNotFoundError:
            print("No existe el archivo productos.txt, se creará uno nuevo al guardar.")

    def guardar_productos(self):
        with open("productos.txt", "w", encoding="utf-8") as archivo:
            for id_producto, datos in self.productos.items():
                fecha = datos.fecha_caducidad if datos.fecha_caducidad else ""
                archivo.write(f"{id_producto}:{datos.nombre}:{datos.id_categoria}:{datos.precio}:{datos.stock}:{fecha}\n")

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
                self.guardar_productos()
                print(f"Producto '{nombre}' agregado correctamente con ID {id_producto}.")
            except ValueError:
                print("Error: Uno de los valores ingresados no tiene el formato correcto.")

    def actualizar_producto(self, id_producto, nuevo_precio=None, nuevo_stock=None):
        id_producto = int(id_producto)
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
                        nit, nombre, telefono, direccion, correo = linea.split(":")
                        self.clientes[nit] = Clientes(nit, nombre, telefono, direccion, correo)
            print("Clientes importados desde clientes.txt")
        except FileNotFoundError:
            print("No existe el archivo clientes.txt, se creará uno nuevo al guardar.")

    def guardar_clientes(self):
        with open("clientes.txt", "w", encoding="utf-8") as archivo:
            for nit, datos in self.clientes.items():
                archivo.write(f"{nit}:{datos.nombre}:{datos.telefono}:{datos.direccion}:{datos.correo}\n")

    def agregar_cliente(self):
        try:
            nit = int(input("Ingrese el NIT del cliente: "))
            nombre = input("Ingrese el nombre del cliente: ").strip()
            telefono = int(input("Ingrese el teléfono del cliente: "))
            direccion = input("Ingrese la dirección del cliente: ")
            correo = input("Ingrese el correo del cliente: ")
            if nit in self.clientes:
                raise CodigoDuplicadoError("El cliente con este NIT ya existe.")
            self.clientes[nit] = Clientes(nit, nombre, telefono, direccion, correo)
            self.guardar_clientes()
            print(f"Cliente con NIT {nit} agregado correctamente.")

        except ValueError:
            print("Error: El teléfono debe ser un número entero.")
        except CodigoDuplicadoError as e:
            print(f"Error de duplicado: {e}")

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
                        id_empleado, nombre, telefono, direccion, correo = linea.split(":")
                        id_empleado = int(id_empleado)
                        self.empleados[id_empleado] = Empleados(id_empleado, nombre, telefono, direccion, correo)
            print("Empleados importados desde Empleados.txt")
        except FileNotFoundError:
            print("No existe el archivo Empleados.txt, se creará uno nuevo al guardar.")

    def guardar_empleados(self):
        with open("Empleados.txt", "w", encoding="utf-8") as archivo:
            for id_empleado, datos in self.empleados.items():
                archivo.write(f"{id_empleado}:{datos.nombre}:{datos.telefono}:{datos.direccion}:{datos.correo}\n")

    def agregar_empleado(self):
        try:
            ide = int(input("Ingrese el ID del empleado: "))
            nombre = input("Ingrese el nombre del empleado: ").strip()
            telefono = int(input("Ingrese el teléfono del empleado: "))
            direccion = input("Ingrese la dirección del empleado: ")
            correo = input("Ingrese el correo del empleado: ")
            if ide in self.empleados:
                raise CodigoDuplicadoError("El empleado con este ID ya existe.")
            self.empleados[ide] = Empleados(ide, nombre, telefono, direccion, correo)
            self.guardar_empleados()
            print("Empleado agregado exitosamente.")
        except ValueError:
            print("Error: El ID y teléfono deben ser números enteros.")
        except CodigoDuplicadoError as e:
            print(f"Error: {e}")

    def eliminar_empleado(self, ide):
        if ide not in self.empleados:
            raise RegistroNoExisteError("No se encontró el empleado.")
        del self.empleados[ide]
        self.guardar_empleados()
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
                        id_proveedor, nombre, empresa, nit, telefono, direccion, correo = linea.split(":")
                        id_proveedor = int(id_proveedor)
                        self.proveedores[id_proveedor] = Proveedores(id_proveedor, nombre, empresa, nit, telefono,
                                                                     direccion, correo)
            print("Proveedores importados desde Proveedores.txt")
        except FileNotFoundError:
            print("No existe el archivo Proveedores.txt, se creará uno nuevo al guardar.")

    def guardar_proveedores(self):
        with open("Proveedores.txt", "w", encoding="utf-8") as archivo:
            for id_proveedor, datos in self.proveedores.items():
                archivo.write(
                    f"{id_proveedor}:{datos.nombre}:{datos.empresa}:{datos.nit}:{datos.telefono}:{datos.direccion}:{datos.correo}\n")

    def agregar_proveedor(self):
        try:
            id_proveedor = int(input("Ingrese el ID del proveedor: "))
        except ValueError:
            print("Error: El ID debe ser un número entero.")
            return
        nombre = input("Ingrese el nombre del proveedor: ").strip()
        empresa = input("Ingrese la empresa del proveedor: ").strip()
        nit = input("Ingrese el NIT del proveedor: ")
        try:
            telefono = int(input("Ingrese el teléfono del proveedor: "))
        except ValueError:
            print("Error: El ID debe ser un número entero.")
            return
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
        self.guardar_proveedores()
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
    def __init__(self, inventario: ManipulacionInventario,clientes,empleados):
        self.inventario = inventario
        self.ventas = {}
        self.detalles_ventas = {}
        self.contador_venta = 1
        self.contador_detalle = 1
        self.clientes = clientes.clientes
        self.empleados =empleados.empleados
        self.cargar_detalles()
        self.cargar_ventas()

    def generar_id_venta(self):
        id_v = self.contador_venta
        self.contador_venta += 1
        return id_v

    def generar_id_detalle(self):
        id_d = self.contador_detalle
        self.contador_detalle += 1
        return id_d

    def guardar_ventas(self):
        with open("ventas.txt", "w", encoding="utf-8") as archivo:
            for id_venta, venta in self.ventas.items():
                archivo.write(f"{venta.id_venta}:{venta.fecha}:{venta.id_cliente}:{venta.id_empleado}:{venta.total}\n")

    def guardar_detalles(self):
        with open("detalles_ventas.txt", "w", encoding="utf-8") as archivo:
            for id_detalle, detalle in self.detalles_ventas.items():
                archivo.write(f"{detalle.id_detalle}:{detalle.id_venta}:{detalle.id_producto}:{detalle.cantidad}:{detalle.precio}:{detalle.subtotal}\n")

    def cargar_ventas(self):
        try:
            with open("ventas.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    if linea.strip():
                        id_venta, fecha, id_cliente, id_empleado, total = linea.strip().split(":")
                        id_venta = int(id_venta)
                        total = float(total)
                        venta = Ventas(id_venta, fecha, id_cliente, id_empleado)
                        venta.total = total
                        self.ventas[id_venta] = venta
                        if id_venta >= self.contador_venta:
                            self.contador_venta = id_venta + 1
            print("Ventas cargadas desde ventas.txt")
        except FileNotFoundError:
            print("No existe ventas.txt, se creará al guardar.")

    def cargar_detalles(self):
        try:
            with open("detalles_ventas.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    if linea.strip():
                        id_detalle, id_venta, id_producto, cantidad, precio, subtotal = linea.strip().split(":")
                        id_detalle = int(id_detalle)
                        id_venta = int(id_venta)
                        id_producto = int(id_producto)
                        cantidad = int(cantidad)
                        precio = float(precio)
                        subtotal = float(subtotal)

                        detalle = DetallesVentas(id_detalle, id_venta, id_producto, cantidad, precio, subtotal)
                        self.detalles_ventas[id_detalle] = detalle

                        if id_venta in self.ventas:
                            self.ventas[id_venta].agregar_detalle(detalle)

                        if id_detalle >= self.contador_detalle:
                            self.contador_detalle = id_detalle + 1
            print("Detalles de ventas cargados desde detalles_ventas.txt")
        except FileNotFoundError:
            print("No existe detalles_ventas.txt, se creará al guardar.")

    def vender(self, id_producto, cantidad, id_cliente=None, id_empleado=None, fecha="hoy"):
        if id_producto not in self.inventario.productos:
            raise RegistroNoExisteError("No se encontró el producto.")

        producto = self.inventario.productos[id_producto]

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}")

        producto.stock -= cantidad

        if id_cliente is None:
            id_cliente = int(input("Ingrese el NIT del cliente: "))
        if id_cliente not in self.clientes:
            print("Cliente no encontrado. La venta se cancelará.")
            return

        if id_empleado is None:
            id_empleado = int(input("Ingrese ID del empleado: "))
        if id_empleado not in self.empleados:
            print("Empleado no válido. La venta se cancelará.")
            return

        id_venta = self.generar_id_venta()
        venta = Ventas(id_venta, fecha, id_cliente, id_empleado)

        id_detalle = self.generar_id_detalle()
        subtotal = cantidad * producto.precio
        detalle = DetallesVentas(id_detalle, id_venta, id_producto, cantidad, producto.precio, subtotal)
        venta.agregar_detalle(detalle)

        self.ventas[id_venta] = venta
        self.detalles_ventas[id_detalle] = detalle
        self.guardar_detalles()
        self.guardar_ventas()

        print(f"Venta registrada. Cliente ID: {id_cliente}, Empleado ID: {id_empleado}")
        print(f"Producto: {producto.nombre}, Cantidad: {cantidad}, Total: Q{subtotal:.2f}")

    def mostrar_historial(self):
        if not self.ventas:
            print("No hay ventas registradas.")
            return
        total_general = 0
        for venta in self.ventas.values():
            print(f"Venta ID: {venta.id_venta} | Fecha: {venta.fecha}")
            for det in venta.detalles:
                print(f"  Producto {det.id_producto} - Cant: {det.cantidad} - Total: Q{det.subtotal:.2f}")
                total_general += det.subtotal
        print(f"\nTotal acumulado de ventas: Q{total_general:.2f}")

    def filtrar_por_codigo(self, codigo):
        ventas_filtradas = []
        for venta in self.ventas.values():
            for det in venta.detalles:
                if det.id_producto == int(codigo):
                    ventas_filtradas.append(det)
        if not ventas_filtradas:
            print("No hay ventas para ese producto.")
            return
        for det in ventas_filtradas:
            print(det.mostrar_detalle())

class DetallesCompras:
    def __init__(self, id_detalle, id_compra, id_producto, cantidad, precio_unitario, subtotal):
        self.id_detalle = id_detalle
        self.id_compra = id_compra
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal

    def calcular_subtotal(self):
        self.subtotal = self.cantidad * self.precio_unitario

    def mostrar_detalle(self):
        return f"Detalle {self.id_detalle}: Producto {self.id_producto} | Cant: {self.cantidad} | Precio compra: Q{self.precio_unitario:.2f} | Subtotal: Q{self.subtotal:.2f}"

    def actualizar_cantidad(self, nueva_cantidad):
        if nueva_cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        self.cantidad = nueva_cantidad
        self.calcular_subtotal()

    def actualizar_precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.precio_unitario= nuevo_precio
        self.calcular_subtotal()

class Compras:
    def __init__(self, id_compra, fecha, id_proveedor, id_empleado):
        self.id_compra = id_compra
        self.fecha = fecha
        self.id_proveedor = id_proveedor
        self.id_empleado = id_empleado
        self.detalles = []
        self.total = 0

    def agregar_detalle(self, detalle: DetallesCompras):
        self.detalles.append(detalle)
        self.total += detalle.subtotal

    def mostrar_compra(self):
        print(f"ID Compra: {self.id_compra}")
        print(f"Fecha: {self.fecha}")
        print(f"ID Proveedor: {self.id_proveedor}")
        print(f"ID Empleado: {self.id_empleado}")
        print("Detalles:")
        for d in self.detalles:
            print(f"ID Producto: {d.id_producto}, Cantidad: {d.cantidad}, Precio: {d.precio_unitario}, Subtotal: {d.subtotal}")

class ManipulacionCompras:
    def __init__(self, inventario: ManipulacionInventario,proveedores,empleados):
        self.inventario = inventario
        self.compras = {}
        self.detalles_compras = {}
        self.contador_compra = 1
        self.contador_detalle = 1
        self.cargar_detalles()
        self.cargar_compras()
        self.proveedores = proveedores.proveedores
        self.empleados = empleados.empleados

    def generar_id_compra(self):
        id_c = self.contador_compra
        self.contador_compra += 1
        return id_c

    def generar_id_detalle(self):
        id_d = self.contador_detalle
        self.contador_detalle += 1
        return id_d

    def guardar_compras(self):
        with open("compras.txt", "w", encoding="utf-8") as archivo:
            for id_compra, compra in self.compras.items():
                archivo.write(f"{compra.id_compra}:{compra.fecha}:{compra.id_proveedor}:{compra.id_empleado}:{compra.total}\n")

    def guardar_detalles(self):
        with open("detalles_compras.txt", "w", encoding="utf-8") as archivo:
            for id_detalle, detalle in self.detalles_compras.items():
                archivo.write(f"{detalle.id_detalle}:{detalle.id_compra}:{detalle.id_producto}:{detalle.cantidad}:{detalle.precio_unitario}:{detalle.subtotal}\n")

    def cargar_compras(self):
        try:
            with open("compras.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    if linea.strip():
                        id_compra, fecha, id_proveedor, id_empleado, total = linea.strip().split(":")
                        id_compra = int(id_compra)
                        total = float(total)
                        compra = Compras(id_compra, fecha, id_proveedor, id_empleado)
                        compra.total = total
                        self.compras[id_compra] = compra
                        if id_compra >= self.contador_compra:
                            self.contador_compra = id_compra + 1
            print("Compras cargadas desde compras.txt")
        except FileNotFoundError:
            print("No existe compras.txt, se creará al guardar.")

    def cargar_detalles(self):
        try:
            with open("detalles_compras.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    if linea.strip():
                        id_detalle, id_compra, id_producto, cantidad, precio_compra, subtotal = linea.strip().split(":")
                        id_detalle = int(id_detalle)
                        id_compra = int(id_compra)
                        id_producto = int(id_producto)
                        cantidad = int(cantidad)
                        precio_compra = float(precio_compra)
                        subtotal = float(subtotal)

                        detalle = DetallesCompras(id_detalle, id_compra, id_producto, cantidad, precio_compra, subtotal)
                        self.detalles_compras[id_detalle] = detalle

                        if id_compra in self.compras:
                            self.compras[id_compra].agregar_detalle(detalle)

                        if id_detalle >= self.contador_detalle:
                            self.contador_detalle = id_detalle + 1
            print("Detalles de compras cargados desde detalles_compras.txt")
        except FileNotFoundError:
            print("No existe detalles_compras.txt, se creará al guardar.")

    def registrar_compra(self, manipulacion_proveedores, manipulacion_empleados, manipulacion_categorias):
        id_compra = self.generar_id_compra()
        fecha = input("Ingrese la fecha: ")

        id_proveedor = int(input("Ingrese el ID del proveedor: "))
        if id_proveedor not in manipulacion_proveedores.proveedores:
            print(f"Error: No existe un proveedor con ID {id_proveedor}")
            return

        id_empleado = int(input("Ingrese el ID del empleado que registró la compra: "))
        if id_empleado not in manipulacion_empleados.empleados:
            print(f"Error: No existe un empleado con ID {id_empleado}")
            return

        compra = Compras(id_compra, fecha, id_proveedor, id_empleado)

        while True:
            id_producto = int(input("Ingrese el ID del producto (o '0' para terminar): "))
            if id_producto == 0:
                break

            if id_producto not in self.inventario.productos:
                print("El producto no está registrado en inventario.")
                opcion = input("¿Desea registrarlo ahora? (s/n): ").strip().lower()
                if opcion == "s":
                    nombre = input("Ingrese el nombre del producto: ").strip()

                    if not manipulacion_categorias.categoria:
                        print("No hay categorías registradas. Agregue primero una categoría.")
                        continue

                    print("Categorías disponibles:")
                    for c in manipulacion_categorias.categoria.values():
                        print(f"ID: {c.id_categoria} | Nombre: {c.nombre}")

                    id_categoria = int(input("Ingrese el ID de la categoría del producto: "))
                    if id_categoria not in manipulacion_categorias.categoria:
                        print("La categoría no existe. Producto no registrado.")
                        continue

                    precio = float(input("Ingrese el precio de venta del producto: "))
                    stock = 0
                    fecha_caducidad = input("Ingrese la fecha de caducidad (opcional): ").strip()

                    id_producto = self.inventario.generar_id()
                    nuevo_producto = Productos(id_producto, nombre, id_categoria, precio, stock, fecha_caducidad)
                    self.inventario.productos[id_producto] = nuevo_producto
                    self.inventario.guardar_productos()
                    print(f"Producto '{nombre}' agregado con ID {id_producto}.")
                else:
                    print("No se puede agregar este producto a la compra.")
                    continue

            cantidad = int(input("Ingrese la cantidad: "))
            precio_compra = float(input("Ingrese el precio de compra: "))
            producto = self.inventario.productos[id_producto]
            subtotal = cantidad * precio_compra

            id_detalle = self.generar_id_detalle()
            detalle = DetallesCompras(id_detalle, id_compra, id_producto, cantidad, precio_compra, subtotal)
            compra.agregar_detalle(detalle)
            self.detalles_compras[id_detalle] = detalle

            producto.stock += cantidad

        self.compras[id_compra] = compra
        self.guardar_detalles()
        self.guardar_compras()
        print(f"Compra registrada exitosamente. Total: Q{compra.total:.2f}")

class Buscar:
    def buscar_valor(self, lista, criterio, valor):
        resultados = []
        valor = valor.lower()
        for item in lista:
            if criterio == "id" and str(item.id_producto) == valor:
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
    def menu_inicio(self,sistema):
        while True:
            print("\n--- SISTEMA DE ACCESO ---")
            print("1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = input("Usuario: ")
                password = input("Contraseña: ")
                usuario = sistema.login(nombre, password)
                if usuario:
                    print(f"\nBienvenido {usuario.nombre} ({usuario.rol})")
                    return usuario
                else:
                    print(" Usuario o contraseña incorrectos.")

            elif opcion == "2":
                nombre = input("Nuevo usuario: ")
                password = input("Nueva contraseña: ")
                print("Roles disponibles: Administrador, Empleado, Bodeguero")
                rol = input("Rol: ")
                try:
                    sistema.registrar(nombre, password, rol)
                    print(" Usuario registrado con éxito, ahora puede iniciar sesión.")
                except CodigoDuplicadoError as e:
                    print(e)

            elif opcion == "3":
                print("Saliendo del sistema...")
                exit()
            else:
                print("Opción inválida. Intente de nuevo.")

sistema = SistemaUsuarios()
manipulacion_inventario = ManipulacionInventario()
manipulacion_categorias = ManipulacionCategorias()
manipulacion_clientes = ManipulacionClientes()
manipulacion_empleados = ManipulacionEmpleados()
manipulacion_proveedores = ManipulacionProveedores()
manipulacion_ventas = ManipulacionVentas(manipulacion_inventario,manipulacion_clientes,manipulacion_empleados)
manipulacion_compras = ManipulacionCompras(manipulacion_inventario,manipulacion_proveedores,manipulacion_empleados)
buscador = Buscar()
ordenamiento = Ordenamiento()
menu = Menu()

usuario_actual = None
intentos = 0
while intentos < 3 and usuario_actual is None:
    usuario_actual = menu.menu_inicio(sistema)
    if usuario_actual is None:
        intentos += 1

if usuario_actual is None:
    print("Se agotaron los intentos. Saliendo...")
    exit()

opcion = 0
while True:
    print(f"\n=== MENÚ PRINCIPAL ({usuario_actual.rol}) ===")

    match usuario_actual.rol:
        case "Administrador":
            print("1.  Agregar producto")
            print("2.  Mostrar inventario")
            print("3.  Actualizar producto")
            print("4.  Buscar producto")
            print("5.  Agregar categoría")
            print("6.  Mostrar categorías")
            print("7.  Eliminar categoría")
            print("8.  Agregar empleado")
            print("9. Mostrar empleados")
            print("10. Eliminar empleado")
            print("11. Agregar proveedor")
            print("12. Mostrar proveedores")
            print("13. Eliminar proveedor")
            print("14. Agregar cliente")
            print("15. Mostrar clientes")
            print("16. Registrar venta")
            print("17. Mostrar historial de ventas")
            print("18. Filtrar ventas por producto")
            print("19. Registrar compra")
            print("20. Mostrar historial de compras")
            print("21. Cerrar sesion")
            print("22. Salir")
        case "Empleado":
            print("\n=== SISTEMA DE GESTIÓN DE SUPERMERCADO ===")
            print("1. Registrar venta")
            print("2. Mostrar historial de venta")
            print("3. Busqueda por codigo de venta")
            print("4. Cerrar sesion")
            print("5. Salir")
        case "Bodeguero":
            print("\n=== SISTEMA DE GESTIÓN DE SUPERMERCADO ===")
            print("1. Compra de producto")
            print("2. Registro de compras")
            print("3. Cerrar sesion")
            print("4. Salir")

    try:
        opcion = int(input("Seleccione una opcion: "))
    except ValueError:
        print("Opcion no valida")
        continue

    match usuario_actual.rol:
        case "Administrador":
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
                        try:
                            lista_ordenada = ordenamiento.quick_sort(lista, criterio)
                            for p1 in lista_ordenada:
                                print(p1)
                        except ValueError as e:
                            print(f"Error: {e}")

                case 3:
                    idp = int(input("Ingrese el ID del producto a actualizar: "))
                    entrada_precio = input("Nuevo precio (deje vacío para no cambiar): ")
                    nuevo_precio = float(entrada_precio) if entrada_precio.strip() else None

                    entrada_stock = input("Nuevo stock (deje vacío para no cambiar): ")
                    nuevo_stock = int(entrada_stock) if entrada_stock.strip() else None
                    try:
                        manipulacion_inventario.actualizar_producto(idp, nuevo_precio, nuevo_stock)
                        print("Producto actualizado correctamente.")
                    except Exception as e:
                        print(f"Error: {e}")

                case 4:
                    criterio = input("Buscar por (id_producto/nombre/categoria): ")
                    valor = input("Valor a buscar: ")
                    lista = manipulacion_inventario.obtener_lista()
                    resultados = buscador.buscar_valor(lista, criterio, valor)
                    if resultados:
                        for r in resultados:
                            print(r)
                    else:
                        print("No se encontraron resultados.")

                case 5:
                    manipulacion_categorias.agregar_categoria()

                case 6:
                    if not manipulacion_categorias.categoria:
                        print("No hay categorías registradas.")
                    else:
                        for c in manipulacion_categorias.categoria.values():
                            print(f"ID: {c.id_categoria} | Nombre: {c.nombre}")

                case 7:
                    manipulacion_categorias.eliminar_categoria()

                case 8:
                    try:
                        manipulacion_empleados.agregar_empleado()
                    except Exception as e:
                        print(f"Error: {e}")

                case 9:
                    manipulacion_empleados.mostrar_empleados()

                case 10:
                    ide = int(input("Ingrese el ID del empleado a eliminar: "))
                    try:
                        manipulacion_empleados.eliminar_empleado(ide)
                    except Exception as e:
                        print(f"Error: {e}")

                case 11:
                    try:
                        manipulacion_proveedores.agregar_proveedor()
                    except Exception as e:
                        print(f"Error: {e}")

                case 12:
                    manipulacion_proveedores.mostrar_proveedores()

                case 13:
                    idp = int(input("Ingrese el ID del proveedor a eliminar: "))
                    try:
                        manipulacion_proveedores.eliminar_proveedor(idp)
                    except Exception as e:
                        print(f"Error: {e}")

                case 14:
                    try:
                        manipulacion_clientes.agregar_cliente()
                    except Exception as e:
                        print(f"Error: {e}")

                case 15:
                    manipulacion_clientes.mostrar_clientes()

                case 16:
                    id_producto = int(input("Ingrese ID del producto: "))
                    cantidad = int(input("Ingrese cantidad: "))

                    id_cliente = input("Ingrese ID del cliente (opcional): ")
                    if id_cliente == "":
                        id_cliente = None
                    else:
                        id_cliente = int(id_cliente)

                    id_empleado = input("Ingrese ID del empleado (opcional): ")
                    if id_empleado == "":
                        id_empleado = None
                    else:
                        id_empleado = int(id_empleado)

                    fecha = input("Ingrese fecha (por defecto 'hoy'): ")
                    if fecha == "":
                        fecha = "hoy"

                    try:
                        manipulacion_ventas.vender(id_producto, cantidad, id_cliente, id_empleado, fecha)
                        print("Venta realizada con éxito.")
                    except RegistroNoExisteError as e:
                        print("Error:", e)
                    except ValueError as e:
                        print("Error:", e)

                case 17:
                    manipulacion_ventas.mostrar_historial()

                case 18:
                    codigo = input("Ingrese el código del producto: ")
                    manipulacion_ventas.filtrar_por_codigo(codigo)

                case 19:
                    manipulacion_compras.registrar_compra(manipulacion_proveedores, manipulacion_empleados, manipulacion_categorias)

                case 20:
                    for detalle in manipulacion_compras.detalles_compras.values():
                        print(detalle.mostrar_detalle())

                case 21:
                    print("Saliendo al menu de usuario")
                    menu.menu_inicio(sistema)

                case 22:
                    print("Saliendo del programa")
                    break

                case _:
                    print(" Opción inválida.")
        case "Empleado":
            match int(opcion):
                case 1:
                    id_producto = int(input("Ingrese ID del producto: "))
                    cantidad = int(input("Ingrese cantidad: "))

                    id_cliente = input("Ingrese ID del cliente (opcional): ")
                    if id_cliente == "":
                        id_cliente = None
                    else:
                        id_cliente = int(id_cliente)

                    id_empleado = input("Ingrese ID del empleado (opcional): ")
                    if id_empleado == "":
                        id_empleado = None
                    else:
                        id_empleado = int(id_empleado)

                    fecha = input("Ingrese fecha (por defecto 'hoy'): ")
                    if fecha == "":
                        fecha = "hoy"

                    try:
                        manipulacion_ventas.vender(id_producto, cantidad, id_cliente, id_empleado, fecha)
                        print("Venta realizada con éxito.")
                    except RegistroNoExisteError as e:
                        print("Error:", e)
                    except ValueError as e:
                        print("Error:", e)

                case 2:
                    manipulacion_ventas.mostrar_historial()

                case 3:
                    codigo = input("Ingrese el código del producto: ")
                    manipulacion_ventas.filtrar_por_codigo(codigo)

                case 4:
                    print("Saliendo al menu de usuario")
                    menu.menu_inicio(sistema)

                case 5:
                    print("Saliendo del sistema")
                    break

                case _:
                    print(" Opción inválida.")
        case "Bodeguero":
            match int(opcion):
                case 1:
                    manipulacion_compras.registrar_compra(manipulacion_proveedores, manipulacion_empleados, manipulacion_categorias)

                case 2:
                    for detalle in manipulacion_compras.detalles_compras.values():
                        print(detalle.mostrar_detalle())

                case 3:
                    print("Saliendo al menu de usuario")
                    menu.menu_inicio(sistema)

                case 4:
                    print("Saliendo del programa")
                    break

                case _:
                    print(" Opción inválida.")
