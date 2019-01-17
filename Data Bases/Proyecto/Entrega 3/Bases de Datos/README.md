## Información de los datos

- Para poder lograr ver el saldo actual correctamente, la idea es traspasar todo al mismo tipo de cambio, en este caso, a NebCoins. Para esto se tiene que ver los pagos, transferencias (todo aquí está en NebCoins) y después con los abonos, que están en pesos. La tabla de abonos incluye el valor de una NebCoin en CLP al momento del abono, por lo que se debe calcular cuantas NebCoins alguien ha abonado. Recuerden que para los abonos que vayan ingresando a la base de datos pueden sacar este valor considerando que el precio de una nebcoin es de 0.001 ETH, y utilizando el valor del ETH real hacer el cambio a CLP.

- En la base de datos de Cuotas, en la columa de pagos 0 significa que no fue pagado y 1 que fue pagado. No puede existir una cuota posterior a un pago si la cuota anterior no ha sido pagada. La suma de todos los montos de una cuota tiene que dar lo mismo que el total del pago.

- Para el manejo de Compras, existen multiples tablas:
-- **CompraProducto/CompraServicio:** Tiene como objetivo representar la compra de productos/servicios para un usuario en un fecha asignada. Los servicios tambien poseen una fecha de expieración
-- **RTiendaProducto/RTiendaServicio:** Tiene como objetivo representar el producto/servicio especifico comprado y en caso de los productos, su cantidad dado un pago de la tabla CompraProducto/CompraServicio
