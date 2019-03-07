#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "stack.h"


int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		printf("Modo de uso: ./solver test.txt\n");
		return 0;
	}

	/* Abrimos el archivo input en modo de lectura */
	FILE *input_file = fopen(argv[1], "r");

	/* Abrimos el archivo output en modo de escritura */
	FILE *output_file = fopen("output.txt", "w");

	/* Revisa que el archivo fue abierto correctamente */
	if (!input_file)
	{
		printf("¡El archivo %s no existe!\n", argv[1]);
		return 2;
	}

	/* Definimos y asignamos las constantes del problema */
	int n; int m; int l;
	fscanf(input_file, "%d %d %d", &n, &m, &l);

	Stack ***matrix = malloc(sizeof(Stack**) * n);

	for(int row = 0; row < n; row++)
	{
		matrix[row] = malloc(sizeof(Stack*) * m);

		for(int column = 0; column < m; column++)
		{
			matrix[row][column] = stack_init();
		}
	}

	for (int i = 0; i < l; i++)
	{
		/* Definimos las variables del problema */
		int o; int r; int c; int k;

		/* Leemos cada linea del archivo */
		fscanf(input_file, "%d %d %d %d", &o, &r, &c, &k);

		//////////////// Aqui agrega tu código ///////////////////
		if (o == 0){
			push(matrix[r][c], k);
		}
		else if (o == 1){
			search_ball(matrix[r][c], k, output_file);
		}
	}


	/* Cerramos los archivos correctamente */
	fclose(input_file);
	fclose(output_file);

	///////////////// Recuerda que antes de acabar tu programa debes liberar toda la memoria reservada ///////////////////

	for(int row = 0; row < n; row++) {

		for (int column = 0; column < m; column++){
				destroy(matrix[row][column]);
				free(matrix[row][column]);
		}
		free(matrix[row]);
	}
	free(matrix);

	/* Esta linea indica que el programa termino sin errores*/
	return 0;
}
