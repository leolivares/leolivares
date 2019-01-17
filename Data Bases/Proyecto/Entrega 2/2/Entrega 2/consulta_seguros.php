<?php include 'header.php';?>
<title>Consulta Seguro - NebBank</title>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
 	$query = "SELECT S.id_seguro, S.nombre FROM seguros AS S, (SELECT id_seguro, COUNT(id_usuario) FROM segurousuario GROUP BY id_seguro ORDER BY COUNT(id_usuario) DESC) AS P WHERE S.id_seguro = P.id_seguro LIMIT(1);";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$seguros = $result -> fetchAll();
	echo "<br>";
	echo "<div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID</th><th scope='col'>Nombre</th></tr></thead><tbody>";;
	foreach ($seguros as $seguro) {
		echo "<tr class='table-secondary'><td>$seguro[0]</td><td>$seguro[1]</td></tr>";
	}
	echo "</tbody></table></div>";
?>

<form action="index.php" method="post">
  <button type="submit" class="btn btn-primary">Volver</button>
</form> 
</div>
</body>
</html>