
CANT_REPETICIONES = 1 #Cantidad de repeticiones por escenario
MEDIDA = None #Medida de desempeño (Si es None, verifica todas)

"""
None: Todas las medidas
1: "Promedio Dinero Confiscado"
2: "Cantidad Minima de Productos vendidos en un dia"
3: "Cantidad Maxima de Productos vendidos en un dia"
4: "Cantidad Promedio de Productos vendidos por dia"
5: "Cantidad de confiscaciones por Dr. Jekyll"
6: "Cantidad de confiscaciones por Mr. Hyde"
7: "Numero de llamadas"
8: "Numero de Concha Estereo"
9: "Numero de Temperaturas Extremas"
10: "Cantidad de Luvias de Hamburguesas"
11: "Promedio de almuerzos de 12:00-12:59"
12: "Promedio de almuerzos de 13:00-13:59"
13: "Promedio de almuerzos de 14:00-15:00"
14: "Cantidad de alumnos sin almorzar"
15: "Calidad promedio de productos"
16: "Cantidad de miembros intoxicados"
17: "Cantidad de productos descompuestos"
18: "Promedio de abandonos de cola por dia"
19: "Cantidad promedio de vendedores sin stock"
20: "Cantidad de engaños a Dr. Jekyll"
21: "Cantidad de engaños a Mr. Hyde"
"""

INICIO_PUTRE = 8 # Solo ingresar valores enteros y antes de las 11
LLEGADA_MIEMBROS = 11 #Determina que los miembros llegan desde las 11
INSTALACION = 11 # Determina que los vendedores se instalaran alrededor de las 11
DESCOMPUESTO = 0.4 #Determina la calidad a la que un producto se considera descompuesto