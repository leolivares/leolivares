#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "structs.h"
#include "../random/extensions.h"


Board* init_board(FILE* input){
	Board* board = malloc(sizeof(Board));

	fscanf(input, "%d", &board -> n);

	board -> table = malloc(sizeof(int*) * board->n);

	for (int i = 0; i < board->n; ++i)
	{	
		board -> table[i] = calloc(sizeof(int), board->n);
		for (int j = 0; j < board->n; ++j)
		{
			fscanf(input, "%d,", &board -> table[i][j]);
			if (board -> table[i][j] == 0)
			{
				board -> row = i;
				board -> col = j;
			}
		}
	}


	random_seed(146547);
	board -> random_table = malloc(sizeof(int**) * board->n);

	for (int i = 0; i < board->n; ++i)
	{	
		board -> random_table[i] = malloc(sizeof(int*) * board->n);
		for (int j = 0; j < board->n; ++j)
		{	
			board -> random_table[i][j] = calloc(sizeof(int), board->n*board->n);
			for (int k = 0; k < board->n*board->n; ++k)
			{
				int number = get_random();
				while (number < 0) {
					number = get_random();
				}
				board -> random_table[i][j][k] = number;
			}
		}
	}

	return board;
};


hashTable*  init_hash_table(int initial_capacity, double max){
	hashTable* hash_t = malloc(sizeof(hashTable));

	hash_t -> overload = max;
	hash_t -> capacity = initial_capacity;
	hash_t -> dict = calloc(sizeof(Node), initial_capacity);
	hash_t -> current_qty = 0;

	return hash_t;
}


int hash_board(Board* board, hashTable* hash_t){
	int h = 0;
	for (int i = 0; i < board->n; ++i)
	{
		for (int j = 0; j < board->n; ++j)
		{
			int index = board->table[i][j];
			h = h ^ board->random_table[i][j][index];
		}
	}

	return h%hash_t->capacity;
}


bool add_to_dict(Board* board, hashTable* hash_t, int hash, int* state, int row, int col, int row_p, int col_p){

	bool in_table = false;
	bool checked = false;

	while (!in_table) {

		if (!hash_t->dict[hash].value)
		{

			in_table = true;

			hash_t -> dict[hash].count++;
			hash_t -> current_qty++;
			hash_t -> dict[hash].value = calloc(sizeof(int), board->n*board->n);
			int c = 0;
		    for (int i = 0; i < board->n; ++i)
		    {
		  	  for (int j = 0; j < board->n; ++j)
		  	  {
		  		hash_t -> dict[hash].value[c] = board->table[i][j];
		  		c++;
		  	  }
		    }

		    if (state != NULL)
		    {
		    	hash_t -> dict[hash].parent_op = calloc(sizeof(int), board->n*board->n);
				  for (int i = 0; i < board->n*board->n; ++i)
			   	{
					  hash_t -> dict[hash].parent_op[i] = state[i];
			    }
				  hash_t -> dict[hash].row = row;
				  hash_t -> dict[hash].col = col;
		    }
		}

		else {
			bool equal  = true;
			int c = 0;
		    for (int i = 0; i < board->n; ++i)
		    {
		  	  for (int j = 0; j < board->n; ++j)
		  	  {
		  	  	if (hash_t -> dict[hash].value[c] != board->table[i][j])
		  	  	{
		  	  		equal = false;
		  	  	}
		  		c++;
		  	  }
		    }

		    if (!equal)
		    {
		    	hash++;

		    	if (hash >= hash_t -> capacity)
		    	{
		    		hash = 0;
		    	}
		    }

		    else {
		    	hash_t -> dict[hash].count++;
		    	
				in_table = true;
				checked = true;
		    }

		}
	}

	return checked;

}


void add_to_queue(Queue* queue, int* operation, Board* board){

	if (queue->head_pointer == NULL)
	{
		queue->head_pointer  = malloc(sizeof(QNode));
		queue->head_pointer -> value = malloc(sizeof(int)*board->n*board->n);

		for (int i = 0; i < board->n*board->n; ++i)
		{
			queue->head_pointer -> value[i] = operation[i];
		}

		queue->head_pointer -> next_node = NULL;
		queue->tail_pointer = queue->head_pointer;

	}

	else {
		queue->tail_pointer -> next_node = malloc(sizeof(QNode));
		queue->tail_pointer -> next_node -> value = malloc(sizeof(int)*board->n*board->n);
		queue->tail_pointer = queue->tail_pointer -> next_node;


		for (int i = 0; i < board->n*board->n; ++i)
		{
			queue->tail_pointer -> value[i] = operation[i];
		}

		queue->tail_pointer -> next_node = NULL;
	}

	
}


void get_next_state(Queue* queue, int* state, int n){
	

	for (int i = 0; i < n*n; ++i)
  	{
  		state[i] = queue->head_pointer->value[i];
  	}

	if (queue->head_pointer == queue->tail_pointer)
	{
		free(queue -> head_pointer -> value);
		free(queue -> head_pointer);
		queue->head_pointer = NULL;
		queue->tail_pointer = NULL;		
	}

	else {
		free(queue->head_pointer->value);
		QNode* node = queue->head_pointer;
		queue->head_pointer = queue->head_pointer -> next_node;
		free(node);
	}


}


void get_current_state(Board* board, int* current_state){

	int n = 0;
	for (int i = 0; i < board->n; ++i)
	{
	  for (int j = 0; j < board->n; ++j)
	  {
	  	current_state[n] = board->table[i][j];
	  	n++;
	  }
	}
}



bool is_solved(Board* board){

	bool solved = true;
	int k = 1;
	if (board -> table[(board->n)-1][(board->n)-1] != 0)
	{
		solved = false;
	}

	else
	{
		for (int i = 0; i < board->n; ++i)
		{
			for (int j = 0; j < board->n; ++j)
			{
				
				if (k != (board->n*board->n) && board -> table[i][j] != k)
				{
					solved = false;
				}
				k++;
			}
		}
	
	}
	return solved;
}


int hash_state(Board* board, hashTable* hash_t, int* state) {
	int h = 0;
	int k = 0;
	for (int i = 0; i < board->n; ++i)
	{
		for (int j = 0; j < board->n; ++j)
		{
			int index = state[k];
			h = h ^ board->random_table[i][j][index];
			k++;
		}
	}

	return h%hash_t->capacity;
}


hashTable* rehash_table(hashTable* hash_t, Board* board){
	//Descomentar prints para observar rehash
	// printf("%s\n", "REHASH");
	// printf("%s %d\n",  "Capacidad Max Actual ->", hash_t->capacity);
	// printf("%s %d\n",  "Cantidad Actual de Registros ->", hash_t->current_qty);
	hashTable* new_hash_t = malloc(sizeof(hashTable));

	new_hash_t -> dict = malloc(sizeof(Node)*hash_t->capacity*2);
	new_hash_t -> capacity = hash_t->capacity*2;
	new_hash_t -> overload = hash_t ->overload;
	new_hash_t -> current_qty = hash_t -> current_qty;
	// printf("%s %d\n", "Nueva Capacidad Max ->",new_hash_t->capacity);
	// printf("\n");


	for (int i = 0; i < hash_t->capacity; ++i)
	{
		if (hash_t -> dict[i].value)
		{
			int new_hash = hash_state(board, new_hash_t, hash_t->dict[i].value);

			bool cont = true;

			while (cont) {

				if (new_hash_t -> dict[new_hash].value != NULL)
				{
					new_hash++;
				}
				else {
					cont = false;
				}
			}
			new_hash_t -> dict[new_hash] = hash_t -> dict[i];
		}
	}

	return new_hash_t;
}

void destroy_board(Board* board) {
	for (int i = 0; i < board->n; i++) {
		free(board -> table[i]);
	}
	free(board -> table);
	
	for (int i = 0; i < board->n; ++i)
	{	
		for (int j = 0; j < board->n; ++j)
		{	
			free(board -> random_table[i][j]);
		}
		free(board -> random_table[i]);
	}
	free(board -> random_table);
	
	free(board);
}


void destroy_hash_table(hashTable* hash_t) {
	for (int i = 0; i < hash_t -> capacity; i++) {
		free(hash_t -> dict[i].value);
		free(hash_t -> dict[i].parent_op);
	}
	free(hash_t -> dict);
	free(hash_t);
}


void destroy_queue(Queue* queue) {
	QNode* node = queue -> head_pointer;
	
	while (node) {
		QNode* next_node = node -> next_node;
		free(node -> value);
		free(node);
		node = next_node;
	}
}
