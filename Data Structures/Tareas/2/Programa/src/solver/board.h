#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

typedef struct table_board Board;
typedef struct node Node;
typedef struct cell Cell;


struct table_board 
{
	int width;
	int height;
	struct node **column_rest;
	int col_positive;
	int col_negative;
	struct node **row_rest;
	int row_positive;
	int row_negative;
	struct cell **cell;
};


struct node
{
	int require;
	int current;
};

struct cell
{
	char position;
	int value;
};


Board *board_init(FILE* input);

void destroy_board(Board* board);

bool is_solved(Board* board);

void board_place_magnet(Board* board, int row, int col, int charge);

void update_restrictions(Board* board, int row, int col, int charge);

bool board_is_safe(Board* board, int row, int col, int charge);

void board_remove_magnet(Board* board, int row, int col, int charge);

bool is_solvable(Board* board, int row, int col, int charge, int extra);
