<?php include 'header.php';?>
<title>Abonos - NebBank</title>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
 	$query = "SELECT * FROM abonos ORDER BY id_abono;";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$abonos = $result -> fetchAll();
	echo "<br><div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID</th><th scope='col'>Tarjeta</th><th scope='col'>Cantidad</th><th scope='col'>Valor NBC</th><th scope='col'>Fecha</th></tr></thead><tbody>";
	setlocale(LC_MONETARY, 'es_CL');
	foreach ($abonos as $abono) {
		$number = money_format('%.2n', $abono[2]);
  		echo "<tr class='table-secondary'><td>$abono[0]</td><td>$abono[1]</td><td>$$number</td><td>$abono[3]</td><td>$abono[4]</td></tr>";
	}
	echo "</tbody></table><div>";
?>

<form action="index.php" method="post">
  <button type="submit" class="btn btn-primary">Volver</button>
</form>
</div> 
</body>
</html>