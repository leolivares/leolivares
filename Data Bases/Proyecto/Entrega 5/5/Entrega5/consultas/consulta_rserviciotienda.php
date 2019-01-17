<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    // $id_nuevo = $_POST["id_elegido"];
    $id_tienda = $_GET["tsid"];

     $query = "SELECT *
            FROM servicios s, rtiendaservicio r, tiendadeservicios t
            WHERE s.id_servicio = r.id_servicio
            AND r.id_tienda_s = t.id_tienda_s
            AND t.id_tienda_s = '$id_tienda';";

    $result = $db -> prepare($query);
    $result -> execute();
    $rservicios = $result -> fetchAll();
?>
