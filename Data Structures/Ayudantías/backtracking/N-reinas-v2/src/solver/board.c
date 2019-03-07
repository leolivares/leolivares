#include "board.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include "../watcher/watcher.h"

Board *board_init(int width, int height)
{
    /* Abrimos la interfaz grafica */
    watcher_open(width, height);

    Board* board = malloc(sizeof(Board));
    board->n_queens = 0;
    board->width = width;
    board->height = height;
    board->cell = malloc(sizeof(int * ) * height);
    for (int row = 0; row < height; row++)
    {
        board->cell[row] = malloc(sizeof(int) * width);
        for (int col = 0; col < width; col++)
        {
            board->cell[row][col] = 0;
        }
    }
    return board;
}

void board_place_queen(Board *board, int row, int col)
{
    board->cell[row][col] = 1;
    board->n_queens++;
    watcher_set_cell_type(row, col, QUEEN);
}

void board_remove_queen(Board* board, int row, int col)
{
    board->cell[row][col] = 0;
    board->n_queens--;
    watcher_set_cell_type(row, col, EMPTY);
}

bool board_is_safe(Board* board, int row, int col)
{
    // check up & down
    for (int i = 0; i < board->width; i++)
        if(board->cell[row][i])
            return false;
    // check left & right
    for (int j = 0; j < board->height; j++)
        if (board->cell[j][col])
            return false;

    /* Check upper diagonal on left side */
    for (int i = row, j = col; i >= 0 && j >= 0; i--, j--)
        if (board->cell[i][j])
            return false;

    /* Check lower diagonal on left side */
    for (int i = row, j = col; j >= 0 && i < board->height; i++, j--)
        if (board->cell[i][j])
            return false;

    /* Check upper diagonal on the right side */
    for (int i = row, j = col; i >= 0 && j < board->width; i--, j++)
        if (board->cell[i][j])
            return false;

    /* Check lower diagonal on the right side */
    for (int i = row, j = col; j < board->width && i < board->height; i++, j++)
        if (board->cell[i][j])
            return false;

    return true;
}

void board_destroy(Board * board)
{
    for (int row = 0; row < board->height; row++)
    {
        free(board->cell[row]);
    }
    free(board->cell);
    free(board);
    watcher_close();
}