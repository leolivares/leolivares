import json
import requests
import os


class PrograPedia:

    def __init__(self):

        self.dic = {}
        self.url = "https://en.wikipedia.org/w/api.php?"
        self.path = "PrograPaginas.pp"


    def leer_dict(self, path):
        pass

    def search_wiki(self, word):
        value = requests.get(self.url, params={"action": "query",
                                               "title": word,
                                               "prop": "extracts",
                                               "format": "json",
                                               "explaintext": "",
                                               "export": True})

        id_pag = str(list(value.json()["query"]["pages"].keys())[0])
        my_dict = {word:
                       {"title": word,
                        "id": id_page,
                        "content": value.json()["query"]["pages"][id_pag]["extract"]
                        }}


