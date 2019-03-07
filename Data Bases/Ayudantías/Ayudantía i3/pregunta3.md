# Crear índice

Primero se debía crear el índice sobre el atributo content de los post. No es necesario entregar el comando

```
db.posts.createIndex({"content": "text"})
```

# Consulta 1

Ojo que el nombre de la colección puede ser cualquiera.

```javascript
var cursor = db.i3pubs.find({$text: {$search: "\"Vamos Chile\" \"Gol\" -\"Vamos Colombia\" "}});
cursor.forEach(
  function(post) {
    var content = post["content"];
    var user_id = post["id_persona"];
    var cursorPersonas = db.i3personas.find({"id_persona": user_id}, {});
    while (cursorPersonas.hasNext()) {
      var personaDocument = cursorPersonas.next();
      var name = personaDocument["name"];
      print(content + " - " + name);
    }
  }
);
```

# Consulta 2

Es un join

```javascript
var cursor = db.i3personas.find({},{});
cursor.forEach(
  function(user) {
    var user_name = user["name"];
    var user_id = user["id_persona"];
    var cursorCompras = (db.i3compras.find({"id_persona": user_id, "compras.tipo": "Deporte"}, {}));
    while (cursorCompras.hasNext()) {
      var compraDocument = cursorCompras.next();
      var comprasArray = compraDocument["compras"];
      for (compra in comprasArray) {
        if (comprasArray[compra].tipo == 'Deporte') {
          print(user_name + " - " + comprasArray[compra].producto);
        }
      }
    }
  }
);
```

# Consulta 3

```javascript
var cursor = db.i3pubs.find({$text: {$search: "\"vamo a calmarno\" -\"vamo a evolucionarlo\""}});
cursor.forEach(
  function(post) {
    var content = post["content"];
    var user_id = post["id_persona"];
    var cursorPersonas = db.i3personas.find({"id_persona": user_id}, {});
    while (cursorPersonas.hasNext()) {
      var personaDocument = cursorPersonas.next();
      var name = personaDocument["name"];
      var pid = personaDocument["id_persona"];
      var total = 0;
      var cursorCompras = db.i3compras.find({"id_persona": user_id}, {});
      while (cursorCompras.hasNext()) {
        var compraDocument = cursorCompras.next();
        var comprasArray = compraDocument["compras"];
        for (compra in comprasArray) {
          if (comprasArray[compra].tipo == 'Pokemon') {
            total += comprasArray[compra].valor;
          }
        }
      }
      print(name + " - " + total);
    }
  }
);
```
