<?php include 'header.php';?>
<title>Mayor Dinero Transferido - NebBank</title>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }


 	$query = "SELECT T.id_usuario, T.nombre, T.apellido, SUM(T.monto) FROM (SELECT U.id_usuario, U.nombre, U.apellido, P.monto FROM usuarios AS U, pagos AS P WHERE U.id_usuario = P.id_usuario1 AND P.id_pago NOT IN (SELECT DISTINCT id_pago FROM cuotas) UNION ALL
 	SELECT U.id_usuario, U.nombre, U.apellido, SUM(C.monto) FROM usuarios AS U, cuotas AS C, pagos AS P WHERE U.id_usuario = P.id_usuario1 AND P.id_pago = C.id_pago AND C.pagado = 1 GROUP BY U.id_usuario, U.nombre, U.apellido) AS T GROUP BY T.id_usuario, T.nombre, T.apellido ORDER BY SUM(T.monto) DESC LIMIT (1);";

	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$resultados = $result -> fetchAll();
	echo "<br>";
	echo "<div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID Usuario</th><th scope='col'>Nombre</th><th scope='col'>Apellido</th><th scope='col'>NBC Transferidos</th></tr></thead><tbody>";

	foreach ($resultados as $r) {
		$number = money_format('%.2n', $r[3]);
		echo "<tr class='table-secondary'><td>$r[0]</td><td>$r[1]</td><td>$r[2]</td><td>$number NBC</td></tr>";
	}

	echo "</tbody></table><div>";
?>

<form action="index.php" method="post">
	<button type="submit" class="btn btn-primary">Volver</button>
</form> 
</div>
</body>
</html>