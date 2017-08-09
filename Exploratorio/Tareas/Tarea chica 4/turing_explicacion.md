# Funcionamiento de la Máquina de Turing

Para la codificación de esta máquina, se utilizaron tres cintas.
Como fase inicial se definió el estado "q0"

El proceso para esta máquina de turing, consiste en comparar cada
nodo con sus hijos, y verificar que estos sean mayores que dicho nodo.
Para lograr esto, y como especifican las instrucciones, fue necesario
comparar cada nodo "Ni" con sus respectivos hijos "Ni*2" y "Ni*2+1".

Al entregar un input de un árbol, con números binarios representando cada
nodo, se procede a copiar el primer nodo en la cinta 2. Una vez que está
copiado el número, se escribe un "1" en la cinta 3, simbolizando que estamos
trabajando con el primer nodo. Este "1" se utiliza como referencia
para saber con que número compararemos el nodo de la fila 2. Si tenemos un "1"
en la fila 3, significa que tenemos que pasar por un ".", para llegar al
nodo en la fila 1 con el que compararemos.

Para el proceso de comparación, se alinean los números que se van a coomparar.
Cifra a cifra se verifican. Si el numero de la fila 1 tiene un "1" mientras
que el de la fila 2 tiene un "0", significa que sus hijos son mayores,  por
lo tanto cumplen. Si ambos dígitos son iguales, se comparan los siguientes dos.
Si el dígito en la fila 2 es un "1" y el de la fila 1 es un "0", significa
que no cumple con la condición de min heap binario, por lo tanto, entra
al estado "qrechazar" y el proceso termina.

Si el primer número con que se compara ("Ni*2") cumple con la condición,
se repite el proceso con el nodo ("Ni*2+1). Si ambos cumplen, se elimina
el número de la fila 2. Luego, utilizando los "1" en la fila 3, se
regresa al siguiente nodo en la fila 1. Cada "1" en la fila 3, simboliza un
"." por el cual el cursor de la fila 1 debe pasar para llegar a el nuevo
nodo.

Desde este punto se repite el proceso. Se copia el nuevo número en la
fila 2, a la vez que se agrega otro "1" a la fila 3. Con la fila 3
se encuentran los nodos hijos de este nuevo número. Se procede a comparar
y se verifica con que cumpla con la condición. Del mismo modo, se elimina
el número de la fila 3, y se regresa al próximo nodo en la fila 1.

Por último, si se llega al caso en que se copia un número de la fila 1
en la 2, y no se consigue un número con el cual comparar, significa
que los otros nodos cumplieron con la condición y por lo tanto, el árbol
terminó. En este punto, se entra al estado "qaccept" y culmina el
proceso, entregando como output que el árbol es un min heap binario.

### Nota:
Los "1" de la fila 3 siempre simbolizan la cantidad de "."
en la fila 1 que el cursor debe pasar para llegar al número con el
que se debe comparar, o para conseguir el siguiente nodo que se
copiara en la fila 2.


## Bonus:
En el segundo archivo .txt se encuentra el código para la máquina de turing,
incluyendo el bonus fácil. Para este bonus, se repitió el proceso explicado
anteriormente, sin embargo, al principio del proceso, el algoritmo reescribe
el árbol inicial, de tal manera que todos los nodos tengan una longitud igual
al nodo mas largo.

Para esto, se cuentan las cifras de cada número binario, añadiendo "0" en la cinta 2, obteniendo al final la cantidad de cifras que tiene el número mas largo.
Luego, esta cantidad se pasa a la cinta 3, y se utiliza para reescribir cada numero de la cinta 1 en la cinta 2, pero añadiendo "0"s al comienzo de cada uno,
de tal manera de que todos queden de la misma longitud sin cambiar su valor. Se
eliminan los "0" de la cinta 3, y se reescribe el árbol en la cinta 1. Desde
este punto, comienza el proceso de verficacion ya explicado.
