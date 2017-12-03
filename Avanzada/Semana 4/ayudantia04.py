from collections import defaultdict

class Node:
    def __init__(self):
        self.passed = 0
        self.childs = dict() #Key: Letra ; Value: Nodo

    def add_child(self,palabra):
        self.passed += 1
        if len(palabra) > 0 :
            if palabra[0] not in self.childs :
                self.childs[palabra[0]] = Node()
                self.childs[palabra[0]].add_child(palabra[1:])
            else :
                self.childs[palabra[0]].add_child(palabra[1:])


    def ask_substring(self,palabra):
        if palabra[0] not in self.childs :
            return "La palabra no esta"
        if len(palabra) == 1 :
            passed = self.childs[palabra[0]].passed
            return passed
        else :
            passed = self.childs[palabra[0]].ask_substring(palabra[1:])
            return passed

    def __repr__(self):
        pass


class SuffixTree:
    def __init__(self,word):
        self.childs = dict() #Key: letra ; Value: Nodo
        for i in range(len(word)) :
            self.__add_sufix(word[i:])

    def __add_sufix(self,palabra):
        if palabra[0] in self.childs :
            self.childs[palabra[0]].add_child(palabra[1:])
        else :
            new = Node()
            self.childs[palabra[0]] = new
            new.add_child(palabra[1:])


    def count_aparitions(self,palabra):
        if palabra[0] not in self.childs :
            return "La palabra no esta"
        if len(palabra) == 1 :
            passed = self.childs[palabra[0]].passed
            return "La palabra aparece {} veces".format(passed)
        passed = self.childs[palabra[0]].ask_substring(palabra[1:])
        return "La palabra aparece {} veces".format(passed)


    def __repr__(self):
        pass

    def sprint(self):
        pass


tree = SuffixTree("mapapar")
print(len(tree.childs))
print("P:", tree.childs["p"].passed)
print("A:", tree.childs["a"].passed)
print(tree.count_aparitions("ap"))

a = {"1" : "azul"}
a.update({"2" :"verde"})
print(a)