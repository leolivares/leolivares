# Tarea 04. Simulación
***Leonardo Olivares***

## Simulacion Singular
Para realizar la simulacion de un semestre, con los parametros que aparecen en
"parametros_iniciales.csv", se utilizará el archivo "semester.py". Al correrlo,
comenzará la simulacion inmediatamente, y al final de la misma, mostrara en
consola las estadisticas obtenidas.

Se dejaron algunos prints comentados, para facilitar la revision, en caso de
querer ver como los eventos van ocurriendo.

Algunas variables, que son constantes y que son establecidas por el enunciado,
se encuentran en el archivo "variables.py". Sin embargo la modificacion, de
algunos de estos parametros podria ocasionar errores. Se explicara mas 
adelante.

Cada simulacion tiene un tiempo aproximado de 20 segundos.


## Escenarios
Para realizar la comparacion de los escenarios, se utiliza el archivo
"escenarios.py". Para decidir la cantidad de repeticiones por escenario y 
la medida de desempeño, se utilizan las variables localizadas en "variables.py",
que se explicaran a continuacion.

La consola mostrara en que simulacion y en que escenario se encuentra,
para mostrar que esta avanzando.


###Variable.py
Como se menciono anteriormente, este archivo contiene variables constantes y
variables que modifican el analisis de los escenarios. 

    - REPETICIONES: El valor de esta variable debe ser un entero, que
    indica la cantidad de veces que se simulara cada escenario.
    
    - MEDIDA: Esta variable debe ser un numero entero que representa la
    medida de desempeño que se desea. Dentro del archivo, y como un
    comentario, estan las medidas con su respectivo numero identificador.
    En caso de que esta variable sea None, se entregaran las comparaciones
    de todas las medidas posibles.
    
    - INICIO_PUTRE: Esta variable se encarga de definir, desde que hora se 
    mide la putrefaccion de los productos. Por enunciado, es a las 8 AM,
    sin embargo, con este valor las putrefacciones dan valores muy altos,
    considerando que las compras comienzan alrededor de las 11. En caso de
    desear probar otro valor, no puede ser mayor a 11, ya que podria retornar
    valores negativos.
    
    - LLEGADA_MIEMBROS e INSTALACION: Estas son las horas en las que 
    aproximadamente comienzan a llegar los miembros y los vendedores, 
    respectivamente. Por enunciado, estan definidas ambas a las 11.
    
    - DESCOMPUESTO: Este es el valor que se decidio, para considerar que un
    producto esta descompuesto. Se puede modificar. Si el valor de la calidad
    de un producto es <= a 0.4, se considera descompuesto. Sin embargo, por
    la manera en que esta planteado la formula para la putrefaccion, este valor
    siempre es muy pequeño.
    
### Consideraciones para la Estadisticas

En general, para los promedios, no se consideraron los fines de semana, solo
los dias hábiles.

Para la cantidad minima vendida en un dia, no se consideran los dias con
lluvias de hamburguesas, ya que siempre seria 0.

Para la calidad promedio de los productos, se consideraron solo las calidades
de los productos que se vendieron, y con los valores al momento de venderse.

Para la cantidad de productos descompuestos, se consideran aquellos productos,
que la venderse, tengan una putrefaccion mayor o igual a 0.75.

#### Observaciones Finales

En cuanto, a las calidades y putrefacciones. Se menciono en un issue que se 
dejara de esta manera. Como las putrefacciones minimas comienzan en un valor
tan alto, las calidades son extremadamente pequeñas, lo que ocasiona que al
momento de la llegada de un Carabinero, la cantidad de vendedores fiscalizados
sea practicamente todos. Se podria cambiar el parametro a las INICIO_PUTRE a las
11, los valores mejorarian, pero casi nada.
