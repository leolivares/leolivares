<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }

 	$query_product_stores = "SELECT nombre, rubro, id_tienda, ubicacion, correo
                           FROM tiendadeproductos";

	$result = $db -> prepare($query_product_stores);
	$result -> execute();
	$tiendas_productos = $result -> fetchAll();


////////////////////////////////////////////////////////////////////////////////

  $query_service_stores = "SELECT nombre, rubro, id_tienda_s, ubicacion, correo
                           FROM tiendadeservicios";

  $result = $db -> prepare($query_service_stores);
  $result -> execute();
  $tiendas_servicios = $result -> fetchAll();


?>
