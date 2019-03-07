#include "../watcher/watcher.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include "board.h"


bool solver(Board* board, int row, int col)
{
	if (is_solved(board))
	{
		return true;
	}

	if (board -> cell[row][col].position == 'T' || board -> cell[row][col].position == 'L')
	{
		for (int charge = -1; charge < 2; charge++)
		{
			if (board_is_safe(board, row, col, charge) &&  is_solvable(board, row, col, charge, 1))
			{
				board_place_magnet(board, row, col, charge);

				int new_col = col;
				int new_row = row;

				if (col + 1 < board -> width)
				{
					new_col = col + 1;
					new_row = row;
				}
				else if (row + 1 < board -> height)
				{
					new_row = row + 1;
					new_col = 0;
				}
				if (solver(board, new_row, new_col))
					return true;

				if (charge != 0)
				{
					board_remove_magnet(board, row, col, charge);
				}
			}
		}
	}

	else
	{

		if (!is_solvable(board, row, col, board -> cell[row][col].value, 0))
		{
			return false;
		}
		else
		{
			int new_col = col;
			int new_row = row;

			if (col + 1 < board -> width)
			{
				new_col = col + 1;
				new_row = row;
			}
			else if (row + 1 < board -> height)
			{
				new_row = row + 1;
				new_col = 0;
			}

			else
			{
				return false;
			}

			if (solver(board, new_row, new_col))
			{
				return true;
			}
		}
		
	}
	return false;
}


int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		printf("Modo de uso: %s test.txt\n", argv[0]);
		return 0;
	}

	FILE* input = fopen(argv[1], "r");

	Board* board = board_init(input);

	watcher_load_layout(argv[1]);

	solver(board, 0, 0);

	watcher_close();
	
	destroy_board(board);
	
	fclose(input);
	
	return 0;
}
