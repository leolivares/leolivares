<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    // $id_nuevo = $_POST["id_elegido"];
    $id_tienda_p = $_GET["tpid"];

 	    $query_tp = "SELECT *
               FROM tiendadeproductos
               WHERE id_tienda= '$id_tienda_p';";

	$result = $db -> prepare($query_tp);
	$result -> execute();
	$tienda_p = $result -> fetchAll();


  $store = $tienda_p[0];

?>
