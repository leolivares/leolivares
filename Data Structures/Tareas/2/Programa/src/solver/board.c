#include "../watcher/watcher.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include "board.h"


Board *board_init(FILE* input)
{
  // Inicializamos el tablero
  Board* board = malloc(sizeof(Board));
  fscanf(input, "%d %d", &board -> width, &board -> height);

  // Inicializamos una matriz con las restricciones de las columnas
  board -> column_rest = malloc(sizeof(Node*) * 2);
  for (int row = 0; row < 2; row++)
  {
    board -> column_rest[row] = calloc(sizeof(Node), board -> width);
  }

  // Inicializamos una matriz con las restricciones de las filas
  board -> row_rest = malloc(sizeof(Node*) * 2);
  for (int row = 0; row < 2; row++)
  {
    board -> row_rest[row] = calloc(sizeof(Node), board -> height);
  }

  // Agregamos las restricciones positivas de las columnas
  board -> col_positive = 0;
  for (int i = 0; i < board -> width; i++) {
    fscanf(input, "%d ", &board -> column_rest[0][i].require);
    if (board -> column_rest[0][i].require != 0)
      board -> col_positive = board -> col_positive + board -> column_rest[0][i].require;
  }
  
  // Agregamos las restricciones negativas de las columnas
  board -> col_negative = 0;
  for (int i = 0; i < board -> width; i++) {
    fscanf(input, "%d ", &board -> column_rest[1][i].require);
    if (board -> column_rest[1][i].require != 0)
      board -> col_negative = board -> col_negative + board -> column_rest[1][i].require;
  }
  
  // Agregamos las restricciones positivas de las filas
  board -> row_positive = 0;
  for (int i = 0; i < board -> height; i++) {
    fscanf(input, "%d ", &board -> row_rest[0][i].require);
    if (board -> row_rest[0][i].require != 0)
      board -> row_positive = board -> row_positive + board -> row_rest[0][i].require;
  }
  
  // Agregamos las restricciones negativas de las filas
  board -> row_negative = 0;
  for (int i = 0; i < board -> height; i++) {
    fscanf(input, "%d ", &board -> row_rest[1][i].require);
    if (board -> row_rest[1][i].require != 0)
      board -> row_negative = board -> row_negative + board -> row_rest[1][i].require;
  }

  // Guardamos la informacion de las celdas en el tablero
  board -> cell = malloc(sizeof(Cell*) * board -> height);
  for (int row = 0; row < board -> height; row++)
  {
    board -> cell[row] = calloc(sizeof(Cell), board -> width);
  }

  for (int i = 0; i < board -> height; i++) 
  {
    for (int j = 0; j < board -> width; j++) 
    {
      fscanf(input, "%c ", &board -> cell[i][j].position);
    }
  }
  return board;
}


void destroy_board(Board* board)
{
  // Libera la memoria de las restricciones por columnas
  for (int row = 0; row < 2; row++)
    {
      free(board -> column_rest[row]);
    }
    free(board -> column_rest);

    // Libera la memoria de las restricciones por filas
    for (int row = 0; row < 2; row++)
    {
      free(board -> row_rest[row]);
    }
    free(board -> row_rest);

    // Libera la memoria del tablero
    for (int i = 0; i < board -> height; i++) 
    {
      free(board -> cell[i]);
    }
    free(board -> cell);
    
    free(board);
}


bool is_solved(Board* board)
{ 
  if (board -> col_positive == 0 && board -> col_negative == 0 &&
      board -> row_positive == 0 && board -> row_negative == 0)
  {
    return true;
  }
  return false;
}


void board_place_magnet(Board* board, int row, int col, int charge)
{
  int row2 = row + 1;
  int col2 = col;
  char vertical = true;
  if (board -> cell[row][col].position == 'L')
  {
    row2 = row;
    col2 = col + 1;
    vertical = false;
  }

  bool positive = true;
  if (charge == -1)
  {
    positive = false;
  }

  board -> cell[row][col].value = charge;
  board -> cell[row2][col2].value = charge * (-1);
  if (charge != 0)
  {
    update_restrictions(board, row, col, charge);
    watcher_set_magnet(row, col, vertical, positive);
    //sleep(1);
  }
}


void update_restrictions(Board* board, int row, int col, int charge)
{

  int row2 = row + 1;
  int col2 = col;
  if (board -> cell[row][col].position == 'L')
  {
    row2 = row;
    col2 = col + 1;
  }

  if (charge == 1)
  {
    if (board -> column_rest[0][col].require > 0)
    {
      board -> column_rest[0][col].current = (board -> column_rest[0][col].current) + 1;
      board -> col_positive = (board -> col_positive) - 1;
    }

    if (board -> row_rest[0][row].require > 0)
    {
      board -> row_rest[0][row].current = (board -> row_rest[0][row].current) + 1;
      board -> row_positive = (board -> row_positive) - 1;
    }

    if (board -> column_rest[1][col2].require > 0)
    {
      board -> column_rest[1][col2].current = (board -> column_rest[1][col2].current) + 1;
      board -> col_negative = (board -> col_negative) - 1;
    }

    if (board -> row_rest[1][row2].require > 0)
    {
      board -> row_rest[1][row2].current = (board -> row_rest[1][row2].current) + 1;
      board -> row_negative = (board -> row_negative) - 1;
    }

  }
  else if (charge == -1)
  {
    if (board -> column_rest[1][col].require > 0)
    {
      board -> column_rest[1][col].current = (board -> column_rest[1][col].current) + 1;
      board -> col_negative = (board -> col_negative) - 1;
    }

    if (board -> row_rest[1][row].require > 0)
    {
      board -> row_rest[1][row].current = (board -> row_rest[1][row].current) + 1;
      board -> row_negative = (board -> row_negative) - 1;
    }

    if (board -> column_rest[0][col2].require > 0)
    {
      board -> column_rest[0][col2].current = (board -> column_rest[0][col2].current) + 1;
      board -> col_positive = (board -> col_positive) - 1;
    }

    if (board -> row_rest[0][row2].require > 0)
    {
      board -> row_rest[0][row2].current = (board -> row_rest[0][row2].current) + 1;
      board -> row_positive = (board -> row_positive) - 1;
    }
  }
}


bool board_is_safe(Board* board, int row, int col, int charge)
{
  if (charge == 0)
    return true;

  int inverse = charge * (-1);

  int row2 = row + 1;
  int col2 = col;
  if (board -> cell[row][col].position == 'L')
  {
    row2 = row;
    col2 = col + 1;
  }

  if (charge == 1)
  {
    if (board -> column_rest[0][col].require > 0 && board -> column_rest[0][col].require == board -> column_rest[0][col].current)
      return false;
    else if (board -> column_rest[1][col2].require > 0 && board -> column_rest[1][col2].require == board -> column_rest[1][col2].current)
      return false;
    else if (board -> row_rest[0][row].require > 0 && board -> row_rest[0][row].require == board -> row_rest[0][row].current)
      return false;
    else if (board -> row_rest[1][row2].require > 0 && board -> row_rest[1][row2].require == board -> row_rest[1][row2].current)
      return false;
  }
  else if (charge == -1)
  {
    if (board -> column_rest[1][col].require > 0 && board -> column_rest[1][col].require == board -> column_rest[1][col].current)
      return false;
    else if (board -> column_rest[0][col2].require > 0 && board -> column_rest[0][col2].require == board -> column_rest[0][col2].current)
      return false;
    else if (board -> row_rest[1][row].require > 0 && board -> row_rest[1][row].require == board -> row_rest[1][row].current)
      return false;
    else if (board -> row_rest[0][row2].require > 0 && board -> row_rest[0][row2].require == board -> row_rest[0][row2].current)
      return false;
  }

  if (board -> cell[row][col].position == 'T')
  {

    if (col - 1 >= 0 && (board -> cell[row][col-1].value != inverse && board -> cell[row][col-1].value != 0))
      return false;
    else if (col + 1 < board -> width && (board -> cell[row][col+1].value != inverse && board -> cell[row][col+1].value != 0))
      return false;
    else if (row - 1 >= 0 && (board -> cell[row-1][col].value != inverse && board -> cell[row-1][col].value != 0))
      return false;

    if (col2 - 1 >= 0 && (board -> cell[row2][col2-1].value != charge && board -> cell[row2][col2-1].value != 0))
      return false;
    else if (col2 + 1 < board -> width && (board -> cell[row2][col2+1].value != charge && board -> cell[row2][col2+1].value != 0))
      return false;
    else if (row2 + 1 < board -> height && (board -> cell[row2+1][col2].value != charge && board -> cell[row2+1][col2].value != 0))
      return false;
  }

  else if (board -> cell[row][col].position == 'L')
  {
    if (row - 1 >= 0 && board -> cell[row-1][col].value != inverse && board -> cell[row-1][col].value != 0)
      return false;
    else if (row + 1 < board -> height && board -> cell[row+1][col].value != inverse && board -> cell[row+1][col].value != 0)
      return false;
    else if (col - 1 >= 0 && board -> cell[row][col-1].value != inverse && board -> cell[row][col-1].value != 0)
      return false;

    if (row2 - 1 >= 0 && board -> cell[row2-1][col2].value != charge && board -> cell[row2-1][col2].value != 0)
      return false;
    else if (row2 + 1 < board -> height && board -> cell[row2+1][col2].value != charge && board -> cell[row2+1][col2].value != 0)
      return false;
    else if (col2 + 1 < board -> width && board -> cell[row2][col2+1].value != charge && board -> cell[row2][col2+1].value != 0)
      return false;

  }
  return true;
}


void board_remove_magnet(Board* board, int row, int col, int charge)
{
  int row2 = row + 1;
  int col2 = col;
  char vertical = true;
  if (board -> cell[row][col].position == 'L')
  {
    row2 = row;
    col2 = col + 1;
    vertical = false;
  }

  board -> cell[row][col].value = 0;
  board -> cell[row2][col2].value = 0;


  if (charge == 1)
  {
    if (board -> column_rest[0][col].require > 0)
    {
      board -> column_rest[0][col].current = (board -> column_rest[0][col].current) - 1;
      board -> col_positive = (board -> col_positive) + 1;
    }

    if (board -> row_rest[0][row].require > 0)
    {
      board -> row_rest[0][row].current = (board -> row_rest[0][row].current) - 1;
      board -> row_positive = (board -> row_positive) + 1;
    }

    if (board -> column_rest[1][col2].require > 0)
    {
      board -> column_rest[1][col2].current = (board -> column_rest[1][col2].current) - 1;
      board -> col_negative = (board -> col_negative) + 1;
    }

    if (board -> row_rest[1][row2].require > 0)
    {
      board -> row_rest[1][row2].current = (board -> row_rest[1][row2].current) - 1;
      board -> row_negative = (board -> row_negative) + 1;
    }

  }
  else if (charge == -1)
  {
    if (board -> column_rest[1][col].require > 0)
    {
      board -> column_rest[1][col].current = (board -> column_rest[1][col].current) - 1;
      board -> col_negative = (board -> col_negative)+ 1;
    }

    if (board -> row_rest[1][row].require > 0)
    {
      board -> row_rest[1][row].current = (board -> row_rest[1][row].current) - 1;
      board -> row_negative = (board -> row_negative) + 1;
    }

    if (board -> column_rest[0][col2].require > 0)
    {
      board -> column_rest[0][col2].current = (board -> column_rest[0][col2].current) - 1;
      board -> col_positive = (board -> col_positive) + 1;
    }

    if (board -> row_rest[0][row2].require > 0)
    {
      board -> row_rest[0][row2].current = (board -> row_rest[0][row2].current) - 1;
      board -> row_positive = (board -> row_positive) + 1;
    }
  }

  watcher_clear_magnet(row, col, vertical);
  //sleep(1);
}


bool is_solvable(Board* board, int row, int col, int charge, int extra)
{
  bool check_row;
  if (col + 1 == (board -> width))
  {
    check_row = true;
  }
  else if (row + 1 == (board -> height))
  {
    check_row = false;
  }
  else
  {
    return true;
  }


  if (check_row)
  {
    if (charge == 1)
    {
      if (board -> row_rest[0][row].require > 0 && board -> row_rest[0][row].require != (board -> row_rest[0][row].current)+extra)
        return false;
      else if (board -> row_rest[1][row].require > 0 && board -> row_rest[1][row].require != board -> row_rest[1][row].current)
        return false;
    }
    else if (charge == -1)
    {
      if (board -> row_rest[0][row].require > 0 && board -> row_rest[0][row].require != board -> row_rest[0][row].current)
        return false;
      else if (board -> row_rest[1][row].require > 0 && board -> row_rest[1][row].require != (board -> row_rest[1][row].current)+extra)
        return false;
    }
    else
    {
      if (board -> row_rest[0][row].require > 0 && board -> row_rest[0][row].require != board -> row_rest[0][row].current)
        return false;
      else if (board -> row_rest[1][row].require > 0 && board -> row_rest[1][row].require != board -> row_rest[1][row].current)
        return false;
    }
  }
  else
  {
    if (charge == 1)
    {
      if (board -> column_rest[0][col].require > 0 && board -> column_rest[0][col].require != (board -> column_rest[0][col].current)+extra)
        return false;
      else if (board -> column_rest[1][col].require > 0 && board -> column_rest[1][col].require != board -> column_rest[1][col].current)
        return false;
    }
    else if (charge == -1)
    {
      if (board -> column_rest[0][col].require > 0 && board -> column_rest[0][col].require != board -> column_rest[0][col].current)
        return false;
      else if (board -> column_rest[1][col].require > 0 && board -> column_rest[1][col].require != (board -> column_rest[1][col].current)+extra)
        return false;
    }
    else
    {
      if (board -> column_rest[0][col].require > 0 && board -> column_rest[0][col].require != board -> column_rest[0][col].current)
        return false;
      else if (board -> column_rest[1][col].require > 0 && board -> column_rest[1][col].require != board -> column_rest[1][col].current)
        return false;
    }
    
  }
  return true;
}
