<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    // $id_nuevo = $_POST["id_elegido"];
    $id_tienda_s = $_GET["tsid"];

 	$query_tp = "SELECT *
               FROM tiendadeservicios
               WHERE id_tienda_s= '$id_tienda_s';";

	$result = $db -> prepare($query_tp);
	$result -> execute();
	$tienda_s = $result -> fetchAll();


  $s_store = $tienda_s[0];

?>
