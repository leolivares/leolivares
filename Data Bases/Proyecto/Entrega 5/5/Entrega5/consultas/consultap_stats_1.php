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


    // Arroja lista de clientes ordenada de desde quien mas dinero ha gastado
    $query = "SELECT U.id_usuario, U.nombre, SUM(R.cantidad * P.precio) FROM usuarios AS U, rcompraproducto AS R, productos AS P, compraproducto AS CP WHERE U.id_usuario = CP.id_usuario AND CP.id_tienda = '$id_tienda' AND P.id_producto = R.id_producto AND R.id_compra = CP.id_compra GROUP BY U.id_usuario ORDER BY SUM(R.cantidad * P.precio) DESC;";

    $result = $db -> prepare($query);
    $result -> execute();
    $usuarios = $result -> fetchAll();

?>
