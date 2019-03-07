#include "board.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include "../watcher/watcher.h"

Board * board_init(int size)
{
    watcher_open(size, size);
    Board * board = malloc(sizeof(Board));
    board->size = size;
    board->asignaciones = malloc(size * sizeof(int));
    for (int i = 0; i < size; i++)
    {
        board->asignaciones[i] = -1;
    }
    return board;
}

void board_assign(Board * board, int pos, int value)
{
    board->asignaciones[pos] = value;
    watcher_set_cell_type(value, pos, QUEEN);
}

void board_deassign(Board * board, int pos, int value)
{
    board->asignaciones[pos] = -1;
    watcher_set_cell_type(value, pos, EMPTY);
}

bool board_isSafe(Board * board, int pos, int value)
{
    // revisar izquierda
    for (int i = 0; i < pos; i++)
    {
        if (board->asignaciones[i] == value)
        {
            return false;
        }
    }

    // revisar diagonal superior izq
    for (int i = pos, j = value; i >= 0; i--, j--)
    {
        if (board->asignaciones[i] == j)
        {
            return false;
        }
    }
    // revisar diagonal inferior izq
    for (int i = pos, j = value; i >= 0; i--, j++)
    {
        if (board->asignaciones[i] == j)
        {
            return false;
        }
    }
    return true;
}

void board_destroy(Board * board)
{
    free(board->asignaciones);
    free(board);
    watcher_close();
}

