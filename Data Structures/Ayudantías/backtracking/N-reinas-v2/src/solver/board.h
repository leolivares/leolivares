#pragma once
#include <stdbool.h>


typedef struct board Board;

struct board
{
    int n_queens;
    int width;
    int height;
    int **cell;
};

Board *board_init(int height, int width);
void board_destroy(Board* board);

void board_place_queen(Board * board, int row, int col);
void board_remove_queen(Board * board, int row, int col);
bool board_is_safe(Board * board, int row, int col);