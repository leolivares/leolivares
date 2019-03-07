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
 	$query = "SELECT * FROM cuotas ORDER BY id_cuota;";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$cuotas = $result -> fetchAll();
	echo "<br><div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID Cuota</th><th scope='col'>ID Pago</th><th scope='col'>Monto</th><th scope='col'>Fecha Expiración</th><th scope='col'>Estado</th></tr></thead><tbody>";
	setlocale(LC_MONETARY, 'es_CL');
	foreach ($cuotas as $cuota) {
		$number = money_format('%.2n', $cuota[2]);
		if ($cuota[4] == 1) {
			$pagado = "Pagado";
		}
		else {
			$pagado = "Por Pagar";
		}
  		echo "<tr class='table-secondary'><td>$cuota[0]</td><td>$cuota[1]</td><td>$number NBC</td><td>$cuota[3]</td><td>$pagado</td></tr>";;
	}
	echo "</tbody></table></div>";
?>

<form action="index.php" method="post">
  <button type="submit" class="btn btn-primary">Volver</button>
</form>
</div> 
</body>
</html>