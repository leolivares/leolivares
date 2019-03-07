#include <stdio.h>
#include <stdlib.h>

double*** tabla;

double pastillas(int e, int m, int dias)
{
	if(e < 0 || m < 0) return 0;

	double enteras = e;
	double mitades = m;

	double probabilidad = 0;

	// if(tabla[e][m][dias] > 0)
	// {
	// 	return tabla[e][m][dias];
	// }
	if(dias == 0)
	{
		probabilidad = mitades / (enteras + mitades);
	}
	else
	{
		probabilidad += (enteras / (enteras + mitades)) * pastillas(enteras - 1, mitades + 1, dias - 1);
		probabilidad += (mitades / (enteras + mitades)) * pastillas(enteras, mitades - 1, dias - 1);
	}
	// tabla[e][m][dias] = probabilidad;

	return probabilidad;
}

int main(int argc, char const *argv[])
{
	if (argc != 4)
	{
		printf("Modo de uso: ./pastillas <enteras> <mitades> <dias>\n");
		return 0;
	}
	int enteras = atoi(argv[1]);
	int mitades = atoi(argv[2]);
	int dias = atoi(argv[3]);

	int cantidad = enteras + mitades;

	tabla = malloc(sizeof(double**) * (cantidad + 1));
	for(int e = 0; e < cantidad + 1; e++)
	{
		tabla[e] = malloc(sizeof(double*) * (cantidad + 1));
		for(int m = 0; m < cantidad + 1; m++)
		{
			tabla[e][m] = malloc(sizeof(double) * (dias + 1));
			for(int d = 0; d < dias + 1; d++)
			{
				tabla[e][m][d] = -1;
			}
		}
	}

	printf("Dia %d: %lf\n", dias, pastillas(enteras, mitades, dias - 1));

	for(int e = 0; e < cantidad + 1; e++)
	{
		for(int m = 0; m < cantidad + 1; m++)
		{
			free(tabla[e][m]);
		}
		free(tabla[e]);
	}
	free(tabla);

	return 0;
}
