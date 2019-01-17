<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    // $id_nuevo = $_POST["id_elegido"];
    $nombre_nuevo = $_GET["nombre_tienda"];

 	$query = "SELECT *
            FROM tiendadeservicios
            WHERE lower(nombre) LIKE lower('%$nombre_nuevo%');";

	$result = $db -> prepare($query);
	$result -> execute();
	$tiendas_servicios = $result -> fetchAll();

?>
