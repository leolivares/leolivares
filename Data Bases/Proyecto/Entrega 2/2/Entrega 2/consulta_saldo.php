<?php include 'header.php';?>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }

    $id_usuario = $_POST['id_usuario'];

 	$query1 = "SELECT T.id_usuario, T.nombre, T.apellido, SUM(T.monto) FROM (SELECT U.id_usuario, U.nombre, U.apellido, P.monto FROM usuarios AS U, pagos AS P WHERE U.id_usuario = P.id_usuario2 AND U.id_usuario = $id_usuario AND P.id_pago NOT IN (SELECT DISTINCT id_pago FROM cuotas) UNION ALL SELECT U.id_usuario, U.nombre, U.apellido, SUM(C.monto) FROM usuarios AS U, cuotas AS C, pagos AS P WHERE U.id_usuario = P.id_usuario2 AND U.id_usuario = $id_usuario AND P.id_pago = C.id_pago AND C.pagado = 1 GROUP BY U.id_usuario, U.nombre, U.apellido) AS T GROUP BY T.id_usuario, T.nombre, T.apellido;";

 	$query2 = "SELECT T.id_usuario, T.nombre, T.apellido, SUM(T.monto) FROM (SELECT U.id_usuario, U.nombre, U.apellido, P.monto FROM usuarios AS U, pagos AS P WHERE U.id_usuario = P.id_usuario1 AND U.id_usuario = $id_usuario AND P.id_pago NOT IN (SELECT DISTINCT id_pago FROM cuotas) UNION ALL SELECT U.id_usuario, U.nombre, U.apellido, SUM(C.monto) FROM usuarios AS U, cuotas AS C, pagos AS P WHERE U.id_usuario = P.id_usuario1 AND U.id_usuario = $id_usuario AND P.id_pago = C.id_pago AND C.pagado = 1 GROUP BY U.id_usuario, U.nombre, U.apellido) AS T GROUP BY T.id_usuario, T.nombre, T.apellido;";

 	$query3 = "SELECT U.id_usuario, SUM(A.cantidad/A.valor_actual) AS nbc_abonado FROM usuarios AS U, tarjetausuario AS T, abonos AS A WHERE T.id_usuario = U.id_usuario AND T.id_tarjeta = A.id_tarjeta AND U.id_usuario = $id_usuario GROUP BY U.id_usuario;";

 	$query4 = "SELECT id_usuario, nombre, apellido FROM usuarios WHERE usuarios.id_usuario = $id_usuario;";

	$result1 = $db -> prepare($query1);
	$result1 -> execute();
	$cobros = $result1 -> fetchAll();

	$result2 = $db -> prepare($query2);
	$result2 -> execute();
	$pagos = $result2 -> fetchAll();

	$result3 = $db -> prepare($query3);
	$result3 -> execute();
	$abonos = $result3 -> fetchAll();

	$result4 = $db -> prepare($query4);
	$result4 -> execute();
	$usuarios = $result4 -> fetchAll();

	$info = array();

	if ($usuarios) {
		$info[] = $usuarios[0][0];
		$info[] = $usuarios[0][1];
		$info[] = $usuarios[0][2];

		if ($abonos) {
			$info[] = $abonos[0][3];
		}

		else {
			$info[] = 0;
		}

		if ($pagos) {
			$info[] = $pagos[0][3];
		}

		else {
			$info[] = 0;
		}

		if ($cobros) {
			$info[] = $cobros[0][3];
		}

		else {
			$info[] = 0;
		}

		$info[] = $info[3] + $info[5] - $info[4];

	}

	else {
		$info = array("N/A", "USUARIO", "NO EXISTE", 0, 0, 0, 0);
	}

	echo "<br>";
	echo "<div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID Usuario</th><th scope='col'>Nombre</th><th scope='col'>Apellido</th><th scope='col'>Abonos</th><th scope='col'>Cobros</th><th scope='col'>Pagos</th><th scope='col'>Saldo</th></tr></thead><tbody>";


	$number1 = money_format('%.2n', $info[3]);
	$number2 = money_format('%.2n', $info[4]);
	$number3 = money_format('%.2n', $info[5]);
	$number4 = money_format('%.2n', $info[6]);
	echo "<tr class='table-secondary'><td>$info[0]</td><td>$info[1]</td><td>$info[2]</td><td>$number1 NBC</td><td>$number3 NBC</td><td>$number2 NBC</td><td>$number4 NBC</td></tr>";

	echo "</tbody></table><div>";
?>
<form action="index.php" method="post">
	<button type="submit" class="btn btn-primary">Volver</button>
</form> 
</div>
</body>
<title> Saldo de <?php echo $usuarios[0][1]." ".$usuarios[0][2]; ?> - NebBank</title>
</html>