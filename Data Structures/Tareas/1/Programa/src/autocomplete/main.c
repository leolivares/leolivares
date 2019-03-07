#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "trie.h"
#include <string.h>

// Esta linea permite usar MAX_LENGTH como una constante en el programa
// Uso 101 para considerar el caracter que indica el fin de un string
#define MAX_LENGTH 101

int main(int argc, char *argv[])
{
	if (argc != 4)
	{
		printf("Modo de uso: ./solver [database.txt] [queries.txt] [output.txt]\n");
		return 0;
	}
	FILE *database = fopen(argv[1], "r");
	FILE *queries  = fopen(argv[2], "r");
	FILE *output   = fopen(argv[3], "w");

	if (!database || !queries || !output)
	{
		printf("¡Error abriendo los archivos!");
		return 2;
	}

	//// Ejemplo de lectura de strings:

	// Leo el numero de entradas en la base de datos
	int n;
	fscanf(database, "%d", &n);
	
	Trie* trie = init_trie();

	// Para cada entrada:
	for (int i = 0; i < n; i++)
	{
		// Obtengo la frecuencia y el largo
		int freq, length;
		// Ojo que incluyo un espacio en el formato para que no lo considere como parte del string
		fscanf(database, "%d %d ", &freq, &length);

		// Leo el string aprovechando que se el largo maximo
		char chars[MAX_LENGTH];
		fgets(chars, MAX_LENGTH, database);
		
		insert_phrase(trie, chars, freq, length);
	}
	
	int m;
	fscanf(queries, "%d", &m);
	
	for (int i = 0; i < m; i++) {
		
		int length;
		fscanf(queries, "%d ", &length);
		
		char phrase[MAX_LENGTH];
		char result[MAX_LENGTH] = {0};
		
		if (length == 0) {
			autocomplete(phrase, result, trie, length);
		}
		else {
			fgets(phrase, MAX_LENGTH, queries);
			autocomplete(phrase, result, trie, length);
		}
		
		fputs(result, output);

	}
	
	destroy(trie -> root_node);
	free(trie);
	trie = NULL;

	
	fclose(database);
	fclose(queries);
	fclose(output);
	return 0;
}
