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

<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    $id_nuevo = $_POST["id_elegido"];

 	$query = "SELECT * FROM ejercicio_ayudantia where id = $id_nuevo;";

	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$pokemones = $result -> fetchAll();
	echo "<table><tr><th>ID</th><th>Nombre</th><th>Altura</th><th>Peso</th><th>Experiencia Base</th><th>Tipo</th></tr>";
	foreach ($pokemones as $pokemon) {
  		echo "<tr><td>$pokemon[0]</td><td>$pokemon[1]</td><td>$pokemon[2]</td><td>$pokemon[3]</td><td>$pokemon[4]</td><td>$pokemon[5]</td></tr>";
	}
	echo "</table>";


?>

<form action="index.php" method="post">
  <input type="submit" value="Volver">
</form> 
</body>
</html>