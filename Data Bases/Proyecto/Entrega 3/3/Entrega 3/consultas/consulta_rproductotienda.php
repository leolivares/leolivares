<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    // $id_nuevo = $_POST["id_elegido"];
    $id_tienda = $_GET["tpid"];

     $query = "SELECT *
            FROM productos p, rtiendaproducto r, tiendadeproductos t
            WHERE p.id_producto = r.id_producto
            AND r.id_tienda = t.id_tienda
            AND t.id_tienda = '$id_tienda';";

    $result = $db -> prepare($query);
    $result -> execute();
    $rproductos = $result -> fetchAll();
?>
