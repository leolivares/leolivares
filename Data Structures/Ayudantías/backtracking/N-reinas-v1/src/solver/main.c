#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include "board.h"


int assignations = 0;

bool solver(Board * board, int pos)
{
	if (pos == board->size)
		return true;
	
	// para cada valor en el dominio que puede tomar una variable
	for (int value = 0; value < board->size; value++)
	{
		// si es que cumple con el conjunto de restricciones
		// acá pueden hacer un AND (&&) y ingresar su poda si es que usan una
		// por ejemplo: if (board_isSafe(board, pos, value) && board_podaA(board, pos, value) && board_podaB(board, pos, value))
		// así pueden sacarlas facilmente
		if (board_isSafe(board, pos, value)) 
		{
			// realizar la asignacion
			board_assign(board, pos, value);
			assignations++;
			sleep(1);

			// Hacemos la llamada recursiva, con la siguiente variable del conjunto
			// en este caso, pos es la variable actual que asignamos, y pos + 1 es la siguiente variable del conjunto
			if (solver(board, pos + 1))
			{
				// encontramos solucion por esta rama
				return true;
			}

			// No encontramos una solucion por esta rama, desasignamos el valor que tomo la variable y
			// nos movemos al siguiente valor del dominio
			board_deassign(board, pos, value);
			sleep(1);
		}
	}
	// en caso de que no pudimos encontrar una solucion en la rama que estamos, retornamos falso
	return false;
}

int main(int argc, char *argv[])
{
	int size = 7;
	Board * board = board_init(size);

	sleep(1);

	if (solver(board, 0))
	{
		printf("Solución encontrada\n");
	}
	else
	{
		printf("No existe solución\n");
	}
	
	sleep(5);
	printf("Número de asignaciones: %d\n", assignations);
	board_destroy(board);
	return 0;
}
