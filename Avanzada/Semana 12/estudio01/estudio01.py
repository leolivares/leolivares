def fibonacci_generator():
    i = 1
    j = 1
    yield 1
    while True:
        yield i
        copia = i
        i += j
        j = copia

gen = fibonacci_generator()

with open("Archivo1.pdf", "rb") as archivo:
    texto = archivo.read()


i = 0
j = 0
chunks = list()
while i < len(texto):
    i = next(gen) + j
    chunks.append(texto[j:i])
    j = i


chunks_a = bytearray()
for c in chunks:
    chunks_a.extend(c[::-1])

print(chunks_a)

with open("nuevo_pdf.pdf", "wb") as archivo:
    archivo.write(chunks_a)


