# Tarea 06. Prograshop
***Leonardo Olivares***

## Inicio del Programa
Para correr el programa, se debe agregar al directorio "server", una carpeta
con nombre "Imagenes", que contenga las imagenes del servidor.
El server se corre con el archivo server/main.
El cliente se inicia con el archivo client/main.
El cliente debe tener dentro de la carpeta client, el directorio Downloads, para
las descargas que realice. (Esta carpeta se incluyo vacia en github).

## Uso del Edit
Cuando el usuario entra a modo edicion, debe elejir una herramienta.
Presionar blurr, activara el proceso de blurr en la imagen.
Al presionar cut, se debe presionar el lugar de inicio en la imagen donde se desea
cortar, y soltar en el lugar final. (No se observara el rectangulo durante la 
seleccion).
Al presionar paint, aparecera una ventana para seleccionar el color,
luego se debe clickear el lugar que se desea pintar en la imagen.

### Consideraciones
* El blurr se tarda aproximadamente 10 segundos. Varia dependiendo de la cantidad
de bytes de la imagen.
* El cut ocurre en un tiempo mas corto.
* El paint se tarda dependiendo de la cantidad de superficie que deba cambiar de
color.
* En el dashboard se encuentran dos botones de flechas. Esta se encargan de cambiar
las paginas del dashboard. La primera pagina es la designada para las imagenes
iniciales. En la segunda, apareceran las imagenes que el cliente suba durante
esa sesion.

### Posibles fallas
Es posible que al iniciar dos clientes a la vez, ocurra un error de json, y alguno
deba ser reiniciado.

