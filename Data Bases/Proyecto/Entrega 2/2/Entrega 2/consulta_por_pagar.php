<?php include 'header.php';?>
<title>Información Transaccion <?php echo $_POST["id_pago"];?> - NebBank</title>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    $id_pago = $_POST["id_pago"];
 	$query = "SELECT SUM(C.monto) FROM cuotas AS C WHERE C.id_pago = $id_pago AND C.pagado = 0;";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$por_pagar = $result -> fetchAll();

	setlocale(LC_MONETARY, 'it_IT');
	echo "<br>";
	echo "<div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID Transaccion</th><th scope='col'>Por Pagar</th></tr></thead><tbody>";

	foreach ($por_pagar as $p) {
		$number = money_format('%.2n', $p[0]);
		echo "<tr class='table-secondary'><td>$id_pago</td><td>$number NBC</td></tr>";
	}

	echo "</tbody></table><div>";
?>

<form action="index.php" method="post">
	<button type="submit" class="btn btn-primary">Volver</button>
</form> 
</div>
</body>
</html>