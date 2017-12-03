# Tarea 03. Humangi
***Leonardo Olivares***

### Lectura de genomas.txt

Para realizar la lectura del archivo genomas.txt se plantearon dos funciones
generadoras que serán explicadas a continuación. Debido a la longitud del 
archivo, fue necesario idear una manera de evitar sobrecargar el uso de la 
memoria, por lo que no se guarda toda la información del archivo,
solo la necesaria.

Las personas se encuentran en una lista, y su información se almacenó en 
namedtuples. Estas namedtuples contienen, el nombre, apellido, nombre completo,
y adn.

El adn consta de un diccionario, en el que las keys son los tags de las 
caracteristicas, y los values son listas que contienen todos los genes que se 
deben tomar en cuenta para el análisis (segun listas.txt).

Una de las funciones generadoras planteadas, se encarga de devolver los números 
del código genético, en órden.

La segunda función generadora, se encarga de devolver los genes según la 
posición en el código genético. Para este proceso, el código genético se 
encuentra dentro de un generador, en lugar de una lista común, para evitar 
ocupar memoria.


### Testing

Para el testing, se entregaron dos archivos .txt (genomas_testing.txt y 
listas_testing.txt). Estos archivos deben estar en el mismo directorio 
que "testing.py".

En el setUp, se llama a uno de los metodos de la libreria de consultas, que
se encarga de leer los archivos.txt y entregar las personas y las listas.

En el tearDown, se eliminan las variables de personas y listas utilizadas en el
test realizado. 


### BONUS

Para el bonus, es necesario ingresar en la consulta, el tag que se desea
observar en el gráfico bubblechart. Es decir, "GTC" o "GGA". 