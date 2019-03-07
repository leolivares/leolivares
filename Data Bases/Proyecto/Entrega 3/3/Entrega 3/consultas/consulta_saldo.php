<?php

	include_once "includes/psql-config.php";
  	try {
    	$db_bank = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
    	$db_store = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    	echo $e->getMessage();
    }

    $id_usuario = $_SESSION['user_id'];

 	$query1 = "SELECT T.id_usuario, T.nombre, T.apellido, SUM(T.monto) FROM (SELECT U.id_usuario, U.nombre, U.apellido, P.monto FROM usuarios AS U, pagos AS P WHERE U.id_usuario = P.id_usuario2 AND U.id_usuario = $id_usuario AND P.id_pago NOT IN (SELECT DISTINCT id_pago FROM cuotas) UNION ALL SELECT U.id_usuario, U.nombre, U.apellido, SUM(C.monto) FROM usuarios AS U, cuotas AS C, pagos AS P WHERE U.id_usuario = P.id_usuario2 AND U.id_usuario = $id_usuario AND P.id_pago = C.id_pago AND C.pagado = 1 GROUP BY U.id_usuario, U.nombre, U.apellido) AS T GROUP BY T.id_usuario, T.nombre, T.apellido;";

 	$query2 = "SELECT T.id_usuario, T.nombre, T.apellido, SUM(T.monto) FROM (SELECT U.id_usuario, U.nombre, U.apellido, P.monto FROM usuarios AS U, pagos AS P WHERE U.id_usuario = P.id_usuario1 AND U.id_usuario = $id_usuario AND P.id_pago NOT IN (SELECT DISTINCT id_pago FROM cuotas) UNION ALL SELECT U.id_usuario, U.nombre, U.apellido, SUM(C.monto) FROM usuarios AS U, cuotas AS C, pagos AS P WHERE U.id_usuario = P.id_usuario1 AND U.id_usuario = $id_usuario AND P.id_pago = C.id_pago AND C.pagado = 1 GROUP BY U.id_usuario, U.nombre, U.apellido) AS T GROUP BY T.id_usuario, T.nombre, T.apellido;";

 	$query3 = "SELECT U.id_usuario, SUM(A.cantidad/A.valor_nebcoin) AS nbc_abonado FROM usuarios AS U, abonos AS A, tarjetas AS t WHERE U.id_usuario = $id_usuario AND T.id_usuario = U.id_usuario AND T.id_tarjeta = A.id_tarjeta GROUP BY U.id_usuario;";

 	$query5 = "SELECT U.id_usuario, SUM(T.monto) AS cantidad FROM usuarios AS U, transferencias AS T WHERE U.id_usuario = $id_usuario AND T.id_usuario1 = U.id_usuario GROUP BY U.id_usuario;";

 	$query6 = "SELECT U.id_usuario, SUM(T.monto) AS cantidad FROM usuarios AS U, transferencias AS T WHERE U.id_usuario = $id_usuario AND T.id_usuario2 = U.id_usuario GROUP BY U.id_usuario;";

 	$query4 = "SELECT id_usuario, nombre, apellido FROM usuarios WHERE usuarios.id_usuario = $id_usuario;";

 	$result1 = $db_bank -> prepare($query1);
	$result1 -> execute();
	$cobros = $result1 -> fetchAll();

	$result2 = $db_bank -> prepare($query2);
	$result2 -> execute();
	$pagos = $result2 -> fetchAll();

	$result3 = $db_bank -> prepare($query3);
	$result3 -> execute();
	$abonos = $result3 -> fetchAll();

	$result4 = $db_bank -> prepare($query4);
	$result4 -> execute();
	$usuarios = $result4 -> fetchAll();

	$result5 = $db_bank -> prepare($query5);
	$result5 -> execute();
	$t_realizadas = $result5 -> fetchAll();

	$result6 = $db_bank -> prepare($query6);
	$result6 -> execute();
	$t_recibidas = $result6 -> fetchAll();


	$info = array();

	if ($usuarios) {
		$info[] = $usuarios[0][0];
		$info[] = $usuarios[0][1];
		$info[] = $usuarios[0][2];

		if ($abonos) {
			$info[] = $abonos[0][1];
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

		if ($t_realizadas){
			$info[] = $t_realizadas[0][1];
		}
		else {
			$info[] = 0;
		}

		if ($t_recibidas) {
			$info[] = $t_recibidas[0][1];
		}
		else {
			$info[] = 0;
		}

		$info[] = $info[3] + $info[5] - $info[4] + $info[7] - $info[6];

	}

	else {
		$info = array("N/A", "USUARIO", "NO EXISTE", 0, 0, 0, 0);
	}

	$number1 = money_format('%.2n', $info[3]);
	$number2 = money_format('%.2n', $info[4]);
	$number3 = money_format('%.2n', $info[5]);
	$saldo = money_format('%.2n', $info[8]);

?>