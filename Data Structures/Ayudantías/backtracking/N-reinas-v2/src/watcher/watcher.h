#ifndef T3_LIB_WATCHER
#define T3_LIB_WATCHER

#include "../puzzle/cell_type.h"

/** Abre un watcher de las dimensiones especificadas */
void watcher_open(int width, int height);

/** Indica el tipo de celda del mapa en una posicion dada */
void watcher_set_cell_type(int row, int col, CellType type);

/** Cierra el watcher */
void watcher_close();

#endif /* End of include guard: T3_LIB_WATCHER */
