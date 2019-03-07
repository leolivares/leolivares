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

     $query = "SELECT *
            FROM productos
            WHERE id_producto = '$id_producto';";

    $result = $db -> prepare($query);
    $result -> execute();
    $productos = $result -> fetchAll();

    $product = $productos[0];

?>
