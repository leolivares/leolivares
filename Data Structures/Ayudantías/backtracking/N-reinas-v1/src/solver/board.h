#pragma once
#include <stdbool.h>

typedef struct board Board;


struct board {
    int size;
    int *asignaciones;
};


Board * board_init(int size);
void board_assign(Board *board, int pos, int value);
void board_deassign(Board *board, int pos, int value);
bool board_isSafe(Board *board, int pos, int value);
void board_destroy(Board *board);