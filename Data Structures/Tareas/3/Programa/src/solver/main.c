#include <stdio.h>
#include <stdlib.h>
#include "structs.h"
#include "../random/extensions.h"


int main(int argc, char *argv[])
{
  if (argc != 3)
  {
    printf("Modo de uso: ./solver [test.txt] [output.txt]\n");
    printf("Donde:\n");
    printf("\t[test.txt] es el archivo de input\n");
    printf("\t[output.txt] es el nombre del archivo a escribir con el output\n");
    return 0;
  }



  FILE* input = fopen(argv[1], "r");

  int MAX_LOAD = 100000;
  double PROPORTION = 0.5;

  Board* board = init_board(input);

  fclose(input);

  hashTable* hash_t = init_hash_table(MAX_LOAD, PROPORTION);

  Queue queue;
  queue.head_pointer = malloc(sizeof(QNode));
  queue.head_pointer -> value = malloc(sizeof(int)*board->n*board->n);
  queue.tail_pointer = queue.head_pointer;
  queue.tail_pointer -> next_node = NULL;

  int h = hash_board(board, hash_t);

  int* current_state = malloc(sizeof(int)*board->n*board->n);
  get_current_state(board, current_state);


  add_to_dict(board, hash_t, h, NULL, 0, 0, -1, -1);
  hash_t -> dict[h].parent_op = NULL;
  hash_t -> dict[h].row = -1;
  hash_t -> dict[h].col = -1;
  int n = 0;
  for (int i = 0; i < board->n; ++i)
  {
  	for (int j = 0; j < board->n; ++j)
  	{
  		queue.head_pointer -> value[n] = board -> table[i][j];
  		n++;
  	}
  }


  int* state = malloc(sizeof(int)*board->n*board->n);

  bool solved = false;

  while (queue.head_pointer != NULL && !solved) {

  	get_next_state(&queue, state, board->n);

  	int n = 0;
  	for (int i = 0; i < board->n; ++i)
	  	{
	  		for (int j = 0; j < board->n; ++j)
	  		{
	  			board->table[i][j] = state[n];

	  			if (state[n] == 0)
	  			{
	  				board->row = i;
	  				board->col = j;
	  			}
	  			n++;
	  		}
	  }


	int current_hash = hash_state(board, hash_t, state);
	int p_row = hash_t -> dict[current_hash].row;
	int p_col = hash_t -> dict[current_hash].col;

  	for (int i = 0; i < 4; ++i)
  	{	

  		if (!solved)
  		{
  			
	  		
	  		bool checked = true;
	  		//Movimiento hacia arriba
	  		if (i == 0)
	  		{
	  			int row = board -> row-1;
		  		int col = board -> col;
		  		if (row < 0)
		  		{
		  			row = (board -> n) - 1;
		  		}

		  		int value = board -> table[row][col];
		  		board -> table[row][col] = 0;
		  		board -> table[board->row][board->col] = value;

		  		get_current_state(board, current_state);
		  		int hash = hash_board(board, hash_t);

		  		checked = add_to_dict(board, hash_t, hash, state, row, col, p_row, p_col);
		  		if (hash_t -> current_qty >= (hash_t -> overload * hash_t -> capacity))
		  		{
		  			hash_t = rehash_table(hash_t, board);
		  		}
	  		}


	  		//Movimiento derecha

	  		else if (i == 1){
	  			int row = board -> row;
		  		int col = board -> col+1;
		  		if (col >= board->n)
		  		{
		  			col = 0;
		  		}

		  		int value = board -> table[row][col];
		  		board -> table[row][col] = 0;
		  		board -> table[board->row][board->col] = value;
		  		get_current_state(board, current_state);

		  		int hash = hash_board(board, hash_t);

		  		checked = add_to_dict(board, hash_t, hash, state, row, col, p_row, p_col);
		  		if (hash_t -> current_qty >= (hash_t -> overload * hash_t -> capacity))
		  		{
		  			hash_t = rehash_table(hash_t, board);
		  		}
	  		}

	  		//Movimiento abajo

	  		else if (i == 2){
	  			int row = board -> row+1;
		  		int col = board -> col;
		  		if (row >= board->n)
		  		{
		  			row = 0;
		  		}

		  		int value = board -> table[row][col];
		  		board -> table[row][col] = 0;
		  		board -> table[board->row][board->col] = value;

		  		get_current_state(board, current_state);
		  		int hash = hash_board(board, hash_t);

		  		checked = add_to_dict(board, hash_t, hash, state, row, col, p_row, p_col);
		  		if (hash_t -> current_qty >= (hash_t -> overload * hash_t -> capacity))
		  		{
		  			hash_t = rehash_table(hash_t, board);
		  		}
	  		}

	  		//Movimiento izquierda

	  		else if (i == 3){
	  			int row = board -> row;
		  		int col = board -> col-1;
		  		if (col < 0)
		  		{
		  			col = (board->n)-1;
		  		}

		  		int value = board -> table[row][col];
		  		board -> table[row][col] = 0;
		  		board -> table[board->row][board->col] = value;
		  		get_current_state(board, current_state);
		  		int hash = hash_board(board, hash_t);

		  		checked = add_to_dict(board, hash_t, hash, state, row, col, p_row, p_col);
		  		if (hash_t -> current_qty >= (hash_t -> overload * hash_t -> capacity))
		  		{
		  			hash_t = rehash_table(hash_t, board);
		  		}

	  		}

	  		if (is_solved(board))
	  		{
	  			solved = true;
	  		}
	  		

	  		if (!checked && !solved)
	  		{			
	  			add_to_queue(&queue, current_state, board);
	  		}

	  		if (!solved) {
	  			int k = 0;
			  	for (int i = 0; i < board->n; ++i)
				{
				  	for (int j = 0; j < board->n; ++j)
				  	{
				  		board->table[i][j] = state[k];
				  		k++;
				  	}
				}
				get_current_state(board, current_state);
	  		}
	  	}
  	}
  }

  if (solved)
  {
  	
  		FILE *output   = fopen(argv[2], "w");
  		int counter = 1;
  		int index = 0;
  		int results[300];

		bool complete = false;

		int hash = hash_board(board, hash_t);
		int last_hash;
	  	bool is_hash = true;
	    bool cont = true;
	    int g = 0;

	    while (cont){
	  	    for (int i = 0; i < board->n; ++i)
		    {
		  	  for (int j = 0; j < board->n; ++j)
		  	  {
		  		  if (board->table[i][j] != hash_t ->dict[hash].value[g])
		  		  {
		  			  is_hash = false;
		  		  }
		  		  g++;
		  	  }
		    }

		    if (is_hash)
		    {
		  	  cont = false;
		    }
		    else {
		  	  hash++;
		  	  if (hash >= hash_t ->capacity)
		  	  {
		  		  hash = 0;
		  	  }
		  	  g = 0;
		  	  is_hash = true;
		    }
	    }  

	  while (!complete) {

	  	if (hash_t -> dict[hash].parent_op != NULL)
	  	{
		  	results[index] = hash_t -> dict[hash].row;
		  	results[index+1] = hash_t -> dict[hash].col;
		  	index = index + 2;

		  	last_hash = hash;	
	  		hash = hash_state(board, hash_t, hash_t -> dict[hash].parent_op);

	  		bool is_hash = true;
			  bool cont = true;
		  	while (cont){
		  	    for (int i = 0; i < board->n*board->n; ++i)
			    {
			  		if (hash_t -> dict[last_hash].parent_op[i] != hash_t ->dict[hash].value[i])
			  		{
			  			is_hash = false;
			  		}
			    }

			    if (is_hash)
			    {
			  	  cont = false;
			    }
			    else {
			  	  hash++;
			  	  if (hash >= hash_t ->capacity)
			  	  {
			  		  hash = 0;
			  	  }
			  	  is_hash = true;
			  	  counter++;
			    }
		    }
	  	}

	  	else
	  	{
	  		complete = true;
	  	}
	  }

	  index--;
	  fprintf(output,"%d\n",(index+1)/2);
	  for (int i = index; i >= 0; i=i - 2)
	  {		
			fprintf(output, "%d,%d\n", results[i], results[i-1]);
	  }
	  fclose(output);

	}

	else {
		printf("%s\n", "No results");
	}
  
  // destroy_board(board);
  // destroy_hash_table(hash_t);
  // destroy_queue(&queue);
  // free(state);
  // free(current_state);
  

  return 0;
}
