<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }

    $id_tienda = $_GET["tpid"];


    // CONSULTA ARROJA NOMBRE Y CANTIDAD DE VECES VENDIDO DE CADA PRODUCTO,
    // EN ORDEN DEL MAS VENDIDO AL MENOS VENDIDO
    $query = "SELECT p.nombre, SUM(r.cantidad)
            FROM compraproducto c, productos p, rcompraproducto r
            WHERE c.id_tienda = '$id_tienda'
            AND c.id_compra = r.id_compra
            AND p.id_producto = r.id_producto
            GROUP BY p.id_producto
            ORDER BY SUM(r.cantidad) DESC;";

    $result = $db -> prepare($query);
    $result -> execute();
    $productos = $result -> fetchAll();

?>
