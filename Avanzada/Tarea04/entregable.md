# Entregable. Tarea 04
***Leonardo Olivares***

## Lista de Eventos

_Programados_

* Alumnos y Funcionarios almuerzan.**|** Ocurre todos los dias, en los siguientes
horarios dependiendo del miembro UC (13:00-13:59; 14:00-15:00; 12:00:12:59).**|**
Cuando un alumno decide almorzar, ingresa a una fila, en un puesto segun sus
preferencias. El estudiante puede abandonar la cola, si el puesto se queda sin
stock, el tiempo de atencion supera su paciencia o si no tiene dinero suficiente.
Por otro lado, los funcionarios, tienen preferncia por sobre los alumnos. Para 
ambos casos, por ultima instancia, se dirigen a comer al QuickDevil. Los miembros
UC, pueden enfermarse por la comida. Durante este evento, se debe registrar la
cantidad de productos vendidos, cantidad de personas que almuerzan segun la hora,
cantidad de alumnos que no almorzaron, cantidad de miembros intoxicados por 
vendedor, cantidad de miembros que abandonan cola y cantidad de veces que el
vendedor se queda sin stock.

* Miembros llegan al Campus.**|** Ocurre todos los dias, desde las 11:00.**|**
Al llegar una persona, decide si comprar un snack, debido a que pasa por la
entrada.**|**  Del mismo modo, el miembro podria intoxicarse. 

* Miembros deciden ir a comer.**|** Segun la hora en la que almuerza la persona.
**|** Si decide ir a comer, se procede al evento de ir a almorzar.

* Ir a comprar comida.**|** Ocurre cuando la persona decide ir a comer.**|**
Determina el tiempo en el que la persona se tarda en trasladarse. A partir de
ahí, la persona compra el almuerzo.

* Mesada.**|** Ocurre una vez cada 30 días, por alumno.**|** El alumno recibe
la mesada en base a una fórmula.

* Instalar Puestos.**|** Ocurre todos los días, entre las 11:00 y las 11:30.**|**
A partir de la instalación, comienza el proceso de ventas.

* Inspeccion.**|** Ocurre cuando los carabineros son llamados por Devil. **|**
Revisan algunos puestos de vendedores. Piden los permisos del vendedor. Si no
posee permisos, los productos del vendedor son confiscados. Del mismo modo, si
encuentran un producto en mal estado. El vendedor tiene cierta probabilidad
de engañar al carabinero, con respecto a el permiso. En caso de tener que
confiscar los productos, el vendedor se retira de por una cierta cantidad de
dias.

* Bancarrota.**|** Ocurre cuando un vendedor no vende ningún producto durante
20 días seguidos.**|** No vuelve a vender durante el resto de la simulacion.

_No Programados_

* Temperaturas Extremas.**|** Ocurre ciertos días del semestre, según una 
probabilidad.**|** Si la temperatura es calor extremo, los productos aumentan
su putrefacción el doble. Si la temperatura es frío intenso, los productos
disminuyen su calidad a la mitad.

* Cóncha Estereo.**|** Ocurre los viernes según una probabilidad. Si no ocurre
durante cuatro semanas, el viernes de la quinta semana debe ocurrir.**|** La
asistencia a la universidad aumenta ese día. Los vendedores aumentan los precios
un 25%.

* Llegada de Policias.**|** Ocurre siempre que Devil realiza una llamada. **|**
A partir de la llegada de los policias, se realizan inspecciones a ciertos 
puestos de comida.

* Lluvia de Hamburguesas.**|** Ocurre un dia segun una probabilidad. **|**
Ese dia los alumnos quedan satisfechos, y no consumen productos. El dia siguiete
las probabilidades de intoxicacion aumentan el doble.
