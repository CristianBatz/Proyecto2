class CodigoDuplicadoError(Exception):
    pass

class RegistroNoExisteError(Exception):
    pass

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

class Categorias:
    def __init__(self, id_categoria, nombre):
        self.id_categoria = id_categoria
        self.nombre = nombre

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

class Proveedores:
    def __init__(self, id_proveedor, nombre, empresa, nit, telefono, direccion, correo):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.empresa = empresa
        self.nit = nit
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo

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

class ManipulacionInventario:
    pass

class Buscar:
    pass

class Ordenamiento:
    pass

