class BadRequest(Exception):
    def __init__(self, consulta):
        super().__init__("La consulta {} no existe.".format(consulta))


class NotFound(Exception):
    def __init__(self, elemento, tipo):
        super().__init__("{} {} Not Found".format(tipo, str(elemento)))


class NotAcceptable(Exception):
    def __init__(self):
        super().__init__("La consulta no arrojó resultados")


class GenomeError(Exception):
    def __init__(self, persona):
        super().__init__("El genoma de {} presenta errores para esta consulta"
                         .format(persona))
