es_arbol(nil).
es_arbol(arbol(Valor,Izquierda,Derecha)) :- es_arbol(Izquierda) , es_arbol(Derecha).
