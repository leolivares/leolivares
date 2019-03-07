#include "stack.h"
#include <stdlib.h>
#include <stdio.h>


Stack *stack_init()
{
  /* Aqui agrega tu código */
  Stack* pointer_new_stack = calloc(2, sizeof(Node*));
  return pointer_new_stack;
}

void push(Stack* stack, int color)
{
  /* Aqui agrega tu código */
  if (!stack -> last_node_pointer){
    stack -> last_node_pointer = malloc(sizeof(Node));
    stack -> last_node_pointer -> value = color;
    stack -> last_node_pointer -> next_node_pointer = NULL;
    stack -> first_node_pointer = stack -> last_node_pointer;
  }

  else {
    Node* new_node = malloc(sizeof(Node));
    new_node -> next_node_pointer = stack -> first_node_pointer;
    stack -> first_node_pointer = new_node;
    stack -> first_node_pointer -> value = color;
  }
}

int pop(Stack* stack)
{
  /* Aqui agrega tu código */
  if (stack -> first_node_pointer){
    int first_color = stack -> first_node_pointer -> value;
    Node* eliminate_pointer = stack -> first_node_pointer;

    if (stack -> first_node_pointer -> next_node_pointer){
      stack -> first_node_pointer = stack -> first_node_pointer -> next_node_pointer;
      free(eliminate_pointer);
      eliminate_pointer = NULL;
    }

    else {
      free(eliminate_pointer);
      eliminate_pointer = NULL;
      stack -> first_node_pointer = NULL;
      stack -> last_node_pointer = NULL;
    }
    return first_color;
  }
  return -1;
}


void destroy(Stack *stack)
{
  /* Aqui agrega tu código */
  Node* current_node_pointer = stack -> first_node_pointer;
  Node* eliminate_pointer = stack -> first_node_pointer;

  if (current_node_pointer){
    while (current_node_pointer -> next_node_pointer) {
      current_node_pointer = current_node_pointer -> next_node_pointer;
      free(eliminate_pointer);
      eliminate_pointer = current_node_pointer;
    }
    free(eliminate_pointer);
  }
}


/* A continuación puedes crear cualquier función adicional que ayude en la
  implementación de tu programa */

  void search_ball(Stack* stack, int color, FILE* output)
  {
    if (!stack -> last_node_pointer){
      fprintf(output, "%s\n", "vacio");
    }

    else {
      Node* current_node_pointer = stack -> first_node_pointer;

      while (current_node_pointer -> value != color && current_node_pointer -> next_node_pointer){
        current_node_pointer = current_node_pointer -> next_node_pointer;
        fprintf(output, "%d\n", pop(stack));
      }

      int color_pop = pop(stack);
      fprintf(output, "%d\n", color_pop);

      if (color_pop != color){
        fprintf(output, "%s\n", "vacio");
      }
    }
  }
