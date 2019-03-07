#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include "board.h"


int assignations = 0;

bool solver(Board * board)
{
	if (board->n_queens == board->width)
		return true;

	for (int row = 0; row < board->height; row++)
	{
		for (int col = 0; col < board->width; col++)
		{
			if (board_is_safe(board, row, col))
			{
				board_place_queen(board, row, col);
				sleep(1);
				assignations += 1;

				if (solver(board))
					return true;

				board_remove_queen(board, row, col); // backtrack
				sleep(1);
			}
		}
	}
	// no existe asignacion posible
	return false;
}

int main(int argc, char *argv[])
{
	int width = 7;
	int height = width;
	Board *board = board_init(height, width);

	if(!solver(board))
		printf("no existe solución!\n");
	else
		printf("solución encontrada!\n");

	printf("asignaciones: %d\n", assignations);

	sleep(5);

	board_destroy(board);
	return 0;
}
