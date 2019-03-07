#include "trie.h"
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

// Definir funciones aca

Trie* init_trie() {
  Trie* new_trie = malloc(sizeof(Trie));
  new_trie -> root_node = init_node();
  return new_trie;
}


Node* init_node() {
  Node* new_node = calloc(1, sizeof(Node));
  new_node -> is_phrase = false;
  new_node -> has_childs = false;
  return new_node;
}


int normalize(int character) {
  if (character == 32) {
    return 0;
  }
  return (character - 96);
}


void insert_phrase(Trie* trie, char phrase[101], int frequency, int length) {

  Node* current_node = trie -> root_node;

  int i = 0;
  while (phrase[i] != '\n') {

    int number = normalize(phrase[i]);
    if (!current_node -> childs[number]) {
      current_node -> has_childs = true;
      current_node -> childs[number] = init_node();
      current_node -> childs[number] -> character = phrase[i];
    }

    if (frequency > current_node -> max_frequency) {
      current_node -> max_frequency = frequency;
      current_node -> next_child = number;
    }

    current_node = current_node -> childs[number];
    i++;
  }

  current_node -> frequency = frequency;
  current_node -> is_phrase = true;
  if (current_node -> max_frequency < frequency) {
    current_node -> max_frequency = frequency;
  }
}


char* autocomplete(char phrase[101], char result[101], Trie* trie, int length) {
  Node* current_node = trie -> root_node;
  int i = 0;
  strncpy(result, phrase, length);
  result[length] = '\n';
  result[length+1] = '\0';
  while (phrase[i] != '\n' && length > 0) {
    current_node = search_node(current_node, phrase[i]);
    if (!current_node) {
      return result;
    }
    i++;
  }

  int j = length;
  if ((phrase[i] == '\n' && current_node -> frequency != current_node -> max_frequency) || length == 0) {
    while (current_node -> frequency != current_node -> max_frequency) {
      current_node = current_node -> childs[current_node -> next_child];
      result[j] = current_node -> character;
      j++;
    }
  }
  result[j] = '\n';
  result[j+1] = '\0';
  return result;
}


Node* search_node(Node* current_node, char character) {
  int number = normalize(character);
  return current_node -> childs[number];
}


void destroy(Node* current_node) {

  if (!current_node -> has_childs) {
    free(current_node);
    current_node = NULL;
  }
  else {
    for (int i = 0; i < 27; i++) {
      if (current_node -> childs[i]) {
        destroy(current_node -> childs[i]);
      }
    }
    current_node -> has_childs = false;
    free(current_node);
    current_node = NULL;
  }
}
