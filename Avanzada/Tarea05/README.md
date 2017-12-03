# Tarea 05.
***Leonardo Olivares***

## Inicio del programa
El archivo que se debe correr, es el "front_end.py". Una vez iniciado, se 
muestra la pantalla de inicio, en donde se debe ingresar el nombre del jugador.
(En caso de no colocar el nombre, sera Player por default). Luego, se puede
acceder a la tabla de highscores, o a la pantalla principal del juego.

Una vez en la pantalla principal del juego, para que este comience, se debe
presionar el boton START.

## Fin del Juego
Una vez que el jugador muere o se completa el nivel 5, se indica en la pantalla
GAME OVER. Despues de 10 segundos, se cerrara la ventana y se mostrara
la tablas de highscores actualizada.

## Store
Al acceder a la tienda, el juego se pausa. Para continuar, basta con presionar
el boton RESUME. De esta forma, el juego continuara y se cerrara automaticamente
la ventana de la tienda. 

Para realizar compras en la tienda, se arrastra el icono del producto deseado
a los cofres que se encuntran en la misma ventana.

## Inventario
El inventario del personaje esta representado por 5 cofres. Estos se observan 
en la pantalla principal del juego y dentro de la tienda. Los cofres cerrados
simbolizan falta de items. Los abiertos simbolizan un item, y este se detalla 
como una imagen dentro del cofre.

### Funcionalidades sin implementar
* Falto colocar una barra que indique la vida actual de los enemigos.
* Las colisiones ocurren, y los eventos respecto a ellas tambien. Sin embargo
las entidades se atraviesan.

### Algunos detalles a considerar
* Los personajes al aumentar de tamaño, pareciera que atraviesan las murallas.
Sin embargo, no lo hacen, debido a que se obseva respecto a su centro.
* Los escapes y persecuciones ocurren, considerando medidas un poco distintas
a las del enunciado, para que ocurran de mejor manera.
* Los ataques ocurren cuando el centro de cada entidad esta lo suficientemente
cerca, por lo tanto, en ocasiones, dependiendo del tamaño, se debe acercar lo 
suficiente.
* Al comprar en la tienda, se debe tener el puntaje necesario. Al realizar la
transaccion el back-end disminuye el puntaje, pero el cambio se muestra en el 
front-end una vez que el juego continua.
* El nombre se pide el inicio, en lugar de al final.

### Bonus Incluidos
* Se utilizaron sprites distintos a los entregados.
* Se incluyeron efectos de sonido al presionar botones, al interactuar con 
elementos y al comer a un enemigo.
* Se cambio el background de las ventanas.
* Se puede jugar en pantalla completa, sin embargo, la tienda no se ve de la mejor
forma en fullscreen.