class Especie :

    def __init__(self,genes):
        self.genes = genes

    def __repr__(self):
        return self.genes

class MapaGenetico :

    def __init__(self):
        self.especies = dict()

    def agregar_especie(self,id,genes):
        especie = Especie(genes)
        self.especies.update({str(id) : especie})

    def no_comparten(self,id):
        genes = self.especies[str(id)].genes
        genes = genes.split("-")

        especies = list()
        for i in self.especies :
            if str(i) != str(id) :
                especies.append(self.especies[str(i)])

        no_comparten = list()
        for esp in especies :
            g = esp.genes.split("-")
            comparten = False
            for gen in genes :
                if gen in g :
                    comparten = True
            if not comparten :
                no_comparten.append(esp)

        print(self.especies[str(id)].genes)
        for esp in no_comparten :
            print(esp)

    def __repr__(self):
        especies = ""
        for esp in self.especies :
            especies += "Id: " + esp + "  Genes: " + self.especies[esp].genes + "\n"
        return especies

if __name__ == "__main__" :

    mapa = MapaGenetico()

    archivo = open("especies.txt","r")
    lineas = archivo.readlines()
    archivo.close()
    limpio = []
    for linea in lineas :
        limpio.append(linea.strip().split(":"))

    for l in limpio :
        mapa.agregar_especie(l[0].strip(),l[1].strip())

    print(mapa)

    print("---------")

    mapa.no_comparten("022")






