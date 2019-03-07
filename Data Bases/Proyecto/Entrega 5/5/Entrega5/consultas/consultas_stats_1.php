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

    // Arroja lista de clientes ordenada de desde quien mas dinero ha gastado
    $query = "SELECT U.id_usuario, U.nombre, SUM(S.precio)
            FROM usuarios AS U, rcompraservicio AS R, servicios AS S, compraservicio AS CS
            WHERE U.id_usuario = CS.id_usuario
            AND CS.id_tienda_s = '$id_tienda'
            AND S.id_servicio = R.id_servicio
            AND R.id_compraservicio = CS.id_compraservicio
            GROUP BY U.id_usuario
            ORDER BY SUM(S.precio) DESC;";

    $result = $db -> prepare($query);
    $result -> execute();
    $usuarios = $result -> fetchAll();

?>
