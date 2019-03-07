<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    // $id_nuevo = $_POST["id_elegido"];
    $id_producto = $_GET["pid"];

     $query = "SELECT t.nombre, t.rubro, t.id_tienda
            FROM productos p, rtiendaproducto r, tiendadeproductos t
            WHERE p.id_producto = r.id_producto
            AND r.id_tienda = t.id_tienda
            AND p.id_producto = '$id_producto';";

    $result = $db -> prepare($query);
    $result -> execute();
    $rtiendas = $result -> fetchAll();

?>
