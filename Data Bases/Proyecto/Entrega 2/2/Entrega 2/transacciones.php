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
 	$query = "SELECT * FROM pagos ORDER BY id_pago;";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$pagos = $result -> fetchAll();
	echo "<br><div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID Pago</th><th scope='col'>ID Usuario 1</th><th scope='col'>ID Usuario 2</th><th scope='col'>Monto</th><th scope='col'>Fecha</th></tr></thead><tbody>";
	setlocale(LC_MONETARY, 'es_CL');
	foreach ($pagos as $pago) {
		$number = money_format('%.2n', $pago[3]);
  		echo "<tr class='table-secondary'><td>$pago[0]</td><td>$pago[1]</td><td>$pago[2]</td><td>$number NBC</td><td>$pago[4]</td></tr>";;
	}
	echo "</tbody></table></div>";
?>

<form action="index.php" method="post">
  <button type="submit" class="btn btn-primary">Volver</button>
</form>
</div> 
</body>
</html>