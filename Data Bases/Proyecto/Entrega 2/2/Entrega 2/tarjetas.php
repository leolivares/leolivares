<?php include 'header.php';?>
<title>Usuarios - NebBank</title>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
 	$query = "SELECT * FROM tarjetas ORDER BY id_tarjeta;";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$tarjetas = $result -> fetchAll();
	echo "<br><div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID Tarjeta</th><th scope='col'>CVV</th><th scope='col'>Fecha de Expiración</th></tr></thead><tbody>";
	foreach ($tarjetas as $tarjeta) {
  		echo "<tr class='table-secondary'><td>$tarjeta[0]</td><td>$tarjeta[1]</td><td>$tarjeta[2]</td></tr>";;
	}
	echo "</tbody></table></div>";
?>

<form action="index.php" method="post">
  <button type="submit" class="btn btn-primary">Volver</button>
</form>
</div> 
</body>
</html>