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

    $c_id = $_GET["c_id"];
    $product = true;

    $sql = "SELECT cp.id_compra, cp.fecha, tp.id_tienda, tp.nombre, p.nombre, p.precio, r.id_producto, r.cantidad, (p.precio * r.cantidad) AS total FROM compraproducto AS cp, usuarios AS u, tiendadeproductos AS tp, productos AS p, rcompraproducto AS r WHERE u.id_usuario = '$id_usuario' AND cp.id_usuario = '$id_usuario' AND tp.id_tienda = cp.id_tienda AND r.id_producto = p.id_producto AND r.id_compra = cp.id_compra AND cp.id_compra = '$c_id';";

	$get_cp = $db_store -> prepare($sql);
	$get_cp -> execute();
	$compra_p = $get_cp -> fetchAll();

    if (empty($compra_p)) {
        $sql = "SELECT cs.id_compraservicio, s.nombre, ts.nombre, ts.id_tienda_s, SUM(s.precio), cs.fecha_de_compra AS total FROM compraservicio AS cs, usuarios AS u, tiendadeservicios AS ts, servicios AS s, rcompraservicio AS r WHERE u.id_usuario = '$id_usuario' AND cs.id_usuario = '$id_usuario' AND ts.id_tienda_s = cs.id_tienda_s AND r.id_servicio = s.id_servicio AND r.id_compraservicio = cs.id_compraservicio AND cs.id_compraservicio = '$c_id' GROUP BY cs.id_compraservicio, ts.id_tienda_s, ts.nombre, cs.fecha_de_compra, s.nombre;";
        $get_cs = $db_store -> prepare($sql);
        $get_cs -> execute();
        $compra_s = $get_cs -> fetchAll();
        $compra_p = $compra_s;

        $tienda = $compra_s[0][3];
        $fecha = $compra_s[0][5];
        $total = $compra_s[0][4];
        $product = false;
    }
    else {
        $total = 0;
        foreach ($compra_p as $key) {
            $total = $total + $key[8];
        }

        $tienda = $compra_p[0][2];
        $fecha = $compra_p[0][1];
    }


    $direct = False;

    $sql2 = "SELECT c.fecha_expiracion, c.monto, c.pagado FROM pagos AS p, cuotas AS c WHERE c.id_pago = p.id_pago AND p.id_usuario1 = '$id_usuario' AND p.id_usuario2 = '$tienda' AND p.fecha_transaccion = '$fecha' AND p.monto = '$total';";
    $get_cuotas = $db_bank -> prepare($sql2);
    $get_cuotas -> execute();
    $cuotas = $get_cuotas -> fetchAll();

    if (empty($cuotas)) {
        $direct = True;
        $sql2 = "SELECT * FROM pagos AS p WHERE p.id_usuario1 = '$id_usuario' AND p.id_usuario2 = '$tienda' AND p.fecha_transaccion = '$fecha' AND p.monto = '$total';";
        $get_direct = $db_bank -> prepare($sql2);
        $get_direct -> execute();
        $directs = $get_direct -> fetchAll();
    }


?>

