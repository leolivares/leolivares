<!DOCTYPE html>
<html>
<style>
table, th, td {
    border: 1px solid black;
}
</style>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>


<h1>Biblioteca Pokemon</h1>
<p>Aquí podran encontrar información sobre pokemones.</p>

<br>
Consulta por tipos(elemento):
<br>
<form action="Consulta_tipos.php" method="post">
  Tipo:<br/>
  <input type="text" name="tipo_elegido">
  <br/>
  Nombre:<br>
  <input type="text" name="nombre_pokemon">
  <br/><br/>
  <input type="submit" value="Buscar">
</form>
<br>
<br>
Stats por Id:
<br>
<form action="Consulta_Stats.php" method="post">
  Id:<br/>
  <input type="text" name="id_elegido">
  <br/>
  <br/><br/>
  <input type="submit" value="Buscar">
</form>
<br>
<br>
<br>
Consulta Pokemones mas altos:
<form action="Consulta_Altura.php" method="post">
  Altura Limite:<br/>
  <input type="text" name="altura">
  <br/>
  <br/><br/>
  <input type="submit" value="Buscar">
</form>
<br>
</body>
</html>
