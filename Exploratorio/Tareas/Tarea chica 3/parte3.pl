rama([V],arbol(V,nil,nil)).
rama([V|Vf],arbol(V,I,D)) :- V == V , rama(Vf,I) ; rama(Vf,D).

prerama([X],arbol(X,_,_)).
prerama([X|Xf],arbol(X,I,D)) :- X == X , prerama(Xf,I) ; prerama(Xf,D).
