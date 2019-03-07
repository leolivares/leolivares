#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

bool isPalindrome(char* word, int i, int j){
  while (i < j){
    if (word[i] != word[j]){
      return false;
    }
    i++;
    j--;
  }
  return true;
}

// int minPalindrome(char* word, int i, int j){
//   if (isPalindrome(word, i, j)){
//     return 1;
//   }
//   int min = j - i + 2;
//   int pal;
//   for (int k = i; k < j; k++){
//     pal = minPalindrome(word, i, k) + minPalindrome(word, k + 1, j);
//     if (pal < min){
//       min = pal;
//     }
//   }
//   return min;
// }

int minPalindrome(char* word, int i, int j, int** tabla){
  if (tabla[i][j] != -1){
    return tabla[i][j];
  }
  if (isPalindrome(word, i, j)){
    tabla[i][j] = 1;
    return 1;
  }
  int min = j - i + 2;
  int pal;
  for (int k = i; k < j; k++){
    pal = minPalindrome(word, i, k, tabla) + minPalindrome(word, k + 1, j, tabla);
    if (pal < min){
      min = pal;
    }
  }
  tabla[i][j] = min;
  return min;
}

int main(int argc, char *argv[]) {
  if (argc != 2)
  {
    printf("Modo de uso: ./program <word>\n");
    return 0;
  }
  char* word = argv[1];
  int len = strlen(word);
  printf("Tamaño del input: %i\n", len);

  //Parte exponencial
  // printf("Numero de palindromos: %i\n", minPalindrome(word, 0, len - 1));

  // Parte polinommial
  int** tabla = malloc(sizeof(int*) * len);
  for (int i = 0; i < len; i++){
    tabla[i] = malloc(sizeof(int) * len);
    for (int j = 0; j < len; j++){
      tabla[i][j] = -1;
    }
  }
  printf("Numero de palindromos: %i\n", minPalindrome(word, 0, len - 1, tabla));
  for (int i = 0; i < len; i++){
    free(tabla[i]);
  }
  free(tabla);

  return 0;
}
