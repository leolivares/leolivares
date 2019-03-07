#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


typedef struct board_t Board;
typedef struct node Node;
typedef struct hash_table hashTable;
typedef struct queue_node QNode;
typedef struct queue Queue;

struct board_t {
	int n;
	int** table;
	int*** random_table;
	int col;
	int row;
};

struct node {
	int count;
	int* value;
	int* parent_op;
	int row;
	int col;
};

struct hash_table {
	double overload;
	int capacity;
	int current_qty;
	struct node* dict;
};


struct queue_node{
	int* value;
	struct queue_node* next_node;
};

struct queue {
	struct queue_node* head_pointer;
	struct queue_node* tail_pointer;
};


Board* init_board(FILE* input);

hashTable*  init_hash_table(int initial_capacity, double max);

int hash_board(Board* board, hashTable* hash_t);

int hash_state(Board* board, hashTable* hash_t, int* state);

bool add_to_dict(Board* board, hashTable* hash_t, int hash, int* state, int row, int col, int row_p, int col_p);

void add_to_queue(Queue* queue, int* operation, Board* board);

void get_next_state(Queue* queue, int* state, int n);

void get_current_state(Board* board, int* current_state);

bool is_solved(Board* board);

hashTable* rehash_table(hashTable* hash_t, Board* board);

void destroy_board(Board* board);

void destroy_hash_table(hashTable* hash_t);

void destroy_queue(Queue* queue);
