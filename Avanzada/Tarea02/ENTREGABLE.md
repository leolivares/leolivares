#Tarea 02 - Leonardo Olivares

## Estructuras de Datos
Para esta tarea, actualmente se tienen establecidas dos estrucutras de datos propias, con el fin de poder organizar y procesar la información pertinente. Estas serán descritas a cotinuación:

1. Lista Ligada : La primera estructura creada para la tarea es una lista agregada, que se elaboró pensando en usarla como sería una lista de Python común, pero sin heredar ni utilizar nunca directamente el built-in de Python. Para crearla, se utilizó la guía de clase. Se caracteriza por tener una cabeza y una cola. Cada item de esta lista es un nodo (Objeto), que tiene como atributos un valor (puede ser cualquier cosa), y un atributo que especifica si tiene algún item siguiente. En caso de no tener, significa que es la cola de la lista. Se penso esta estructura para cualquier caso en que se necesitaria usar una lista común de Python.

2. Grafo : La segunda estructura planteada fue un grafo, en el cual cada nodo representa una pieza que fue jugada. El nodo principal constituye la pieza random que es obligatoria al comienzo del juego. Cada nodo tiene como atributos, la pieza que representa y las piezas que tiene conectadas a ella. Estas conexiones se mantienen dentro de un instancia de la lista ligada mencionada anteriormente. Se utilizará el nodo como guía para obtener los puntajes, así como también para tener un registro de las piezas que estan conectadas unas con otras.
