<?php include 'header.php';?>
<title>Consulta Abonos - NebBank</title>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
 	$query = "SELECT U.nombre, U.apellido, T.id_tarjeta, A.cantidad FROM usuarios AS U, tarjetas AS T, abonos AS A, tarjetausuario AS P WHERE U.id_usuario = P.id_usuario AND T.id_tarjeta = P.id_tarjeta AND A.id_tarjeta = T.id_tarjeta;";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$abonos = $result -> fetchAll();
	setlocale(LC_MONETARY, 'es_CL');
	echo "<br>";
	echo "<div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>Nombre</th><th scope='col'>Apellido</th><th scope='col'>Tarjeta</th><th scope='col'>Cantidad</th></tr></thead><tbody>";
	foreach ($abonos as $abono) {
		$number = money_format('%.2n', $abono[3]);
  		echo "<tr class='table-secondary'><td>$abono[0]</td><td>$abono[1]</td><td>$abono[2]</td><td>$$number</td></tr>";
	}
	echo "</tbody></table><div>";
?>

<form action="index.php" method="post">
	<button type="submit" class="btn btn-primary">Volver</button>
</form> 
</div>
</body>
</html>