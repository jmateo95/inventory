# Inventory

Este es un sistema de inventarios desarrollado para las empresas que se dedican a la
venta de artículos varios, este tiene la capacidad de manejar usuarios con diferentes tipos de
permisos en la aplicación, además de poder registrar clientes para asociarlos a las
transacciones

El usuario administrador tiene acceso a todas las funciones del sistema, además tiene
acceso a un dashboard para el análisis de datos, los usuarios de bodega pueden ingresar
nuevos productos y proveedores, además de poder actualizar existencias, los usuarios
vendedores tienen el acceso a descontar productos del inventario por medio de ventas
quedando el registro de estas transacciones en facturas dentro del sistema.

**Función Stock Bajo:**

El sistema también tiene la capacidad de notificar cuando los productos llegan a un
punto de reorden. Después de la notificación la aplicación tendrá que buscar entre su lista de
proveedores, el proveedor del producto en específico y pedir una orden de la cantidad
especificada del producto a través de un correo electrónico. Este correo solo es mandado una
vez hasta que se registren los productos manualmente.

**Dashboard:**

El sistema muestra un registro de estadísticas, en la cual se muestran las estadísticas
por cada producto donde se pueden observar los datos como el nombre, cantidad existente,
cantidad mínima permitida (cantidad con la cual se realizará un nuevo pedido).
También cuenta con información acerca de las ventas del mes, ganancias del mes,
además de podrá visualizar por medio de una tabla el inventario general (Este inventario
puede ser descargado en formato PNG) el inventario puede clasificarse por categorías
(Alimentos, Mascotas, etc.)
