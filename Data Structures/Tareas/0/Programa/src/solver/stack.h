#pragma once
#include <stdio.h>


typedef struct stack Stack;

typedef struct node Node;


struct node
{
  /* Aqui agrega tu código */
  int value;
  struct node* next_node_pointer;
};

struct stack
{
  /* Aqui agrega tu código */
  struct node* first_node_pointer;
  struct node* last_node_pointer;
};


Stack *stack_init();

void push(Stack* stack, int color);

int pop(Stack* stack);

void destroy(Stack *stack);

void search_ball(Stack* stack, int color, FILE* output);
