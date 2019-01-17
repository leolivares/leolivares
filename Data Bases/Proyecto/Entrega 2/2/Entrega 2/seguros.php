<?php include 'header.php';?>
<title>Seguros - NebBank</title>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
 	$query = "SELECT * FROM seguros ORDER BY id_seguro;";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$seguros = $result -> fetchAll();
	echo "<br><div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID</th><th scope='col'>Nombre</th><th scope='col'>Descripcion</th></tr></thead><tbody>";
	foreach ($seguros as $seguro) {
  		echo "<tr class='table-secondary'><td>$seguro[0]</td><td>$seguro[1]</td><td>$seguro[2]</td></tr>";
	}
	echo "</tbody></table><div>";
?>

<form action="index.php" method="post">
  <button type="submit" class="btn btn-primary">Volver</button>
</form>
</div> 
</body>
</html>