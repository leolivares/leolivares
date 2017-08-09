abb(nil).
abb(arbol(V,I,D)) :- ordenado(I < V) , ordenado(D > V).
ordenado(arbol(V1,I1,D1)>arbol(V2,I2,D2)) :- V1 > V2 , abb(arbol(V1,I1,D1)) , abb(arbol(V2,I2,D2)).
ordenado(arbol(V1,I1,D1)<arbol(V2,I2,D2)) :- V1 =< V2 , abb(arbol(V1,I1,D1)) , abb(arbol(V2,I2,D2)).
ordenado(arbol(V1,I1,D1)<nil) :- abb(arbol(V1,I1,D1)).
ordenado(arbol(V1,I1,D1)>nil) :- abb(arbol(V1,I1,D1)).
ordenado(arbol(V1,I1,D1)>N) :- V1 > N , abb(arbol(V1,I1,D1)).
ordenado(arbol(V1,I1,D1)<N) :- V1 =< N , abb(arbol(V1,I1,D1)).
ordenado(nil<_).
ordenado(nil>_).
% En caso de ser dos nodos de igual numero, se considerara correcto que se encuentre en la rama iquierda.
