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

     $query = "SELECT t.nombre, t.rubro, t.id_tienda_s
            FROM servicios s, rtiendaservicio r, tiendadeservicios t
            WHERE s.id_servicio = r.id_servicio
            AND r.id_tienda_s = t.id_tienda_s
            AND s.id_servicio= '$id_servicio';";

    $result = $db -> prepare($query);
    $result -> execute();
    $rtiendas = $result -> fetchAll();

?>
