#pragma once
#include <stdbool.h>

/** Carga el archivo a la pantalla */
void watcher_load_layout(char* filename);

/** Elimina el iman de la posicion dada indicando si es un iman vertical u horizontal */
void watcher_clear_magnet(int row, int col, bool vertical);

/** Dibuja un iman en la posicion dada indicando si es vertical u orizontal y si es positivo o negativo */
void watcher_set_magnet(int row, int col, bool vertical, bool positive);

/** Cierra la ventana */
void watcher_close();
