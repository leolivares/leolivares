#include "watcher.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

char** board;
int height;
int width;

/** Carga el archivo a la pantalla */
void watcher_load_layout(char* filename)
{
  // Leo el archivo del test
  FILE* test_file = fopen(filename, "r");

  // Leo el alto y el ancho
  fscanf(test_file, "%d %d\n", &width, &height);

  // Creo el tablero
  board = malloc(sizeof(char*) * height);
  for (int i = 0; i < height; i++)
  {
    board[i] = malloc(sizeof(char) * width);
    for (int j = 0; j < width; j++)
    {
      // Inicializo el tablero vacio
      board[i][j] = 'E';
    }
  }

  // Cierro el archivo
  fclose(test_file);
}

/** Elimina el iman de la posicion dada indicando si es un iman vertical u horizontal */
void watcher_clear_magnet(int row, int col, bool vertical)
{
  board[row][col] = 'E';
  if (vertical) board[row + 1][col] = 'E';
  else board[row][col + 1] = 'E';
}

/** Dibuja un iman en la posicion dada indicando si es vertical u orizontal y si es positivo o negativo */
void watcher_set_magnet(int row, int col, bool vertical, bool positive)
{
  if (positive)
  {
    board[row][col] = 'P';
    if (vertical) board[row + 1][col] = 'N';
    else board[row][col + 1] = 'N';
  }
  else
  {
    board[row][col] = 'N';
    if (vertical) board[row + 1][col] = 'P';
    else board[row][col + 1] = 'P';
  }
}

/** Cierra el watcher */
void watcher_close()
{
  // Escribo en un archivo el resultado
  FILE* out = fopen("output.txt", "w");
  for (int i = 0; i < height; i++)
  {
    for (int j = 0; j < width; j++)
    {
      fprintf(out, "%c ", board[i][j]);
    }
    fprintf(out, "\n");
  }

  // Libero la memoria
  for (int i = 0; i < height; i++)
  {
    free(board[i]);
  }
  free(board);
  fclose(out);
}
