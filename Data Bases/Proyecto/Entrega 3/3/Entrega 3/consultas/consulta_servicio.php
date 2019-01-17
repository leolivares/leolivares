<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    // $id_nuevo = $_POST["id_elegido"];
    $id_servicio = $_GET["sid"];

 	$query = "SELECT *
            FROM servicios
            WHERE id_servicio= '$id_servicio';";

	$result = $db -> prepare($query);
	$result -> execute();
	$servicios = $result -> fetchAll();

    $service = $servicios[0];

?>
