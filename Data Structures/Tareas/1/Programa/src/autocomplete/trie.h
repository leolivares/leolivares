#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// Definir struct aca
typedef struct node Node;
typedef struct trie Trie;


struct node {
  char character;
  struct node* childs[27];
  int next_child;
  bool is_phrase;
  bool has_childs;
  int frequency;
  int max_frequency;
};

struct trie {
  struct node* root_node;
};


// Headers de funciones aca

Trie* init_trie();

Node* init_node();

int normalize(int character);

void insert_phrase(Trie* trie, char phrase[101], int frequency, int length);

void destroy(Node* current_node);

char* autocomplete(char phrase[101], char result[101], Trie* trie, int length);

Node* search_node(Node* current_node, char character);
