# Tarea 03. Entregable

## Lectura del Genoma

Para realizar la lectura del genoma de una persona, se lee el archivo indicado utilizando "with open" y se extraen las lineas. Luego, por cada línea comienza el proceso de lectura, que es el siguiente:

  - Se plantea una función generadora, que a traves de yields retornará, uno por uno, los números que se encuentran en el header.(Número de Nombre, Num de Apellido, Números de listas)

  - Se aplica un filter, para obtener solo las letras del genoma.

  - A partir de los números que retorna la funcion generadora, se extraen las letras correspondientes del filter anterior.

  - Una vez que la información del genoma esta dividida segun sus partes, se almacen en namedtuples, representando a una Persona, con atributos de nombre, apellido, características (dict) y adn (lista).

### Built-ins utilizados para la lectura

  - lambda: Para establecer funciones cortas dentro de maps y filters.

  - map: Para obtener información de los datos en un iterable.

  - filter: Para filtrar el contenido de un iterable a lo necesario.

  - map: Para agrupar en tuplas información necesaria.

### Funciones Atomizadas Necesarias

  - leer_personas(): Lectura del archivo "genoma.txt". LLama por cada linea, a la funcion crear_persona, y el return de esta lo va almacenando en una lista por compresion. Retorna dicha lista de personas (namedtuple)

  - leer_listas(): Lectura del archivo "listas.txt". Crea un diccionario por compresion, en donde cada id de lista es la key, mientras que los values son las listas. Retorna el diccionario.

  - crear_persona(linea: str): Se encarga de manipular el genoma de cada persona, para almacenar la informacion en namedtuples. Esta funcion le entrega toda la linea a funcion_generadora. Divide las partes del genoma, en nombre, apellido, caracateristicas con su respectivas listas, y adn. Retorna la namedtuple.

  - funcion_generadora(linea: str): Esta función recibe el genoma completo, y realiza yield cada vez que obtiene un número con todas sus cifras. Cuando se vuelve a llamar, busca el siguiente numero. Se detiene cuando retorno todos los números posibles.


## Consulta ascendecia(persona)

  - ascendecia(persona): Recibe el nombre de la persona, obtiene la namedtuple correspondiente filtrando la lista de personas. Llama a la funcion analizar_caracteristica(), por cada caracteristica de la persona. Luego con los datos obtenidos, llama a la fúncion determinar_fenotipo, para recibir el fenotipo por cada característica. Por último, llama a la función obtener_ascendecia. Retorna las ascendencias de la persona.

  - analizar_caracteristica(característica, persona): Recibe un tipo de característica, y a partir de la persona, encuentra los genes correspondientes. A partir de ellos, los agrupa en un dicc segun su cantidad. Retorna el diccionario.

  - determinar_fenotipo(dicc, caracteristica): Recibe los datos obetenidos de la funcion anterior, y segun la caracteristica, devuelve el fenotipo adecuado.

  - obtener_ascendecia(valores): Recibe los valores de los fenotipos, y a partir de ellos, realiza las comparaciones necesarias para determinar las ascendencias de la persona.


## Consulta pariente_de(grado, persona)

  -  obtener_datos(): Retorna una lista comprimida con los datos de las cantidades de genes correspondientes por cada caracteristica.

  - gradoX(): Segun el grado, filtra la lista anterior, y retorna a las personas que cumplan con el parentesco.
