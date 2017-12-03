#Informacion y Supuestos de la Tarea 1

##Inicio del Sitema DCC Exchange

Al inicio del programa, el código revisa los archivos .csv entregados, con el fin de extraer la información necesaria para crear los objetos (Mercados, Orders, Usuarios). Inicialmente, el archivo entregado no contiene información acerca del balance de los usuarios, por lo tanto se estableció lo siguiente sobre la lectura inicial de los archivos :
     1. Los usuarios estan registrados solo en los mercados en donde tengan orders.
     2. Como se considera que los usuarios ya estaban registrados en estos mercados, no se les entregan 50.000 de cada moneda, y como estaban en el sistema, tampoco se les entregan los 100.000 DCC.
     3. El balance de estos usuarios iniciales, será 0 en un principio, sin embargo, puede que tengan monedas en alguna order de algun mercado.
     4. Al iniciar el programa y crear las orders, se verificará que estas realicen match de ser posible, por lo tanto, algunos usuarios puede que reciban las monedas que obtuvieron a partir de este match.

## Funcionamiento de las Orders y Matchs

En el momento en que un usuario registra una order (bid o ask), se le extrae de su balance la cantidad de monedas que ofreció (en caso de ser un ask), o la cantidad de monedas que pagará (en caso de ser un bid). Estas monedas seguirán siendo suyas, pero no estarán dentro de su balance para evitar que disponga de ellas nuevamente.

En caso de que lo desee, se cancela la order y recupera sus monedas, solo si la order aún no ha realizado match.

Para los match, se consideraron las distintas posibilidades, pero siempre se busca el beneficio de ambos usuarios. En caso de que un usuario realice una oferta de compra por un cantidad "X" y consiga comprar monedas a un cantidad "Y", tal que X > Y, entonces el sistema se encargará de devolverle al usuario las monedas que no gastó pero que habia entregado al momento de ingresar la order.

El match se considera al momento en que la cantidad de la order llega a 0, y es en ese momento en que recibe la fecha de match. En caso de ser un match parcial, simplemente la cantidad se reduce y la order restante permanece en el mercado.

## Registro de acciones y Eventos

Todos los datos pedidos en el enunciado con respecto a las acciones que realizan los usuarios con sus respectivos tiempos y detalles, estarán en el archivo registros.csv, y se iran agregando a medida que ocurran.

## Salir del sistema

Cuando el usuario finaliza la sesión, se regresa al menú inicial. Es en ese momento en que todos los archivos se actualizan con la nueva información.

### Supuestos y Extras

    - La tasa de los mercados se eligen al azar, siendo un número entre 0,01 y 0,4 ; con el fin de que la comisión no sea tan grande, lo cual haría perder mucho dinero a los usuarios.

    - En la consulta de saldo, se calcula el saldo total en monedas DCC. Para esto se utilizan los valores actuales de las monedas en todos los mercados del tipo "XXXDCC". En caso de no existir un valor actual (es decir, aun no ha ocurrido un match) se toma la relación entre la moneda XXX y DCC como 1-1.

    - El archivo users y orders, después de la primera lectura son sobreescritos. En el caso de users.csv se le añaden columnas nuevas con información relevante.
