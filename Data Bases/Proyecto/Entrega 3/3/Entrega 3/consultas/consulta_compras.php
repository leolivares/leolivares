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

    $sql_productos = "SELECT cp.id_compra, tp.id_tienda, tp.nombre, SUM(p.precio * r.cantidad), cp.fecha AS total FROM compraproducto AS cp, usuarios AS u, tiendadeproductos AS tp, productos AS p, rcompraproducto AS r WHERE u.id_usuario = '$id_usuario' AND cp.id_usuario = '$id_usuario' AND tp.id_tienda = cp.id_tienda AND r.id_producto = p.id_producto AND r.id_compra = cp.id_compra GROUP BY cp.id_compra, tp.id_tienda, tp.nombre, cp.fecha;";


    $sql_servicios = "SELECT cs.id_compraservicio, ts.id_tienda_s, ts.nombre, SUM(s.precio), cs.fecha_de_compra AS total FROM compraservicio AS cs, usuarios AS u, tiendadeservicios AS ts, servicios AS s, rcompraservicio AS r WHERE u.id_usuario = '$id_usuario' AND cs.id_usuario = '$id_usuario' AND ts.id_tienda_s = cs.id_tienda_s AND r.id_servicio = s.id_servicio AND r.id_compraservicio = cs.id_compraservicio GROUP BY cs.id_compraservicio, ts.id_tienda_s, ts.nombre, cs.fecha_de_compra;";



	$get_cp = $db_store -> prepare($sql_productos);
	$get_cp -> execute();
	$compra_p = $get_cp -> fetchAll();


    $get_cs = $db_store -> prepare($sql_servicios);
    $get_cs -> execute();
    $compra_s = $get_cs -> fetchAll();


?>

