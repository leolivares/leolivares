#include "watcher.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void replace_char(char* string, size_t string_size, char out_char, char in_char);

#define WATCHER "./seer"

static FILE* watcher = NULL;

/** Abre un watcher de las dimensiones especificadas */
void watcher_open(int width, int height)
{
  char command[256];
  sprintf(command, "%s %d %d", WATCHER, width, height);

  if(watcher) watcher_close();

  // printf("Ejecutando: %s\n", command);
  watcher = popen(command, "w");
}

/** Indica el tipo de celda del mapa en una posicion dada */
void watcher_set_cell_type(int row, int col, CellType type)
{
	if(watcher)
	{
		if(fprintf(watcher, "CELL %d %d %u\n", row, col, type) < 0)
		{
			watcher_close();
		}
		else
		{
			fflush(watcher);
		}
	}
}

/** Cierra el watcher */
void watcher_close()
{
  if(watcher)
  {
    if(fprintf(watcher, "%s\n", "END") >= 0)
    {
      fflush(watcher);
      pclose(watcher);
    }
    watcher = NULL;
  }
}
