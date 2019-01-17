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


    // Consulta arroja las fechas agrupadas por mes y el monto total
    // recibido por la tienda en ese mes.
    $query = "SELECT date_trunc('month', fecha_de_compra) AS MES, SUM(s.precio)
          FROM tiendadeservicios t, compraservicio c, servicios s, rcompraservicio r
          WHERE t.id_tienda_s = c.id_tienda_s
          AND c.id_compraservicio = r.id_compraservicio
          AND s.id_servicio = r.id_servicio
          AND c.id_tienda_s = '$id_tienda'
          GROUP BY MES
          ORDER BY MES;";

    $result = $db -> prepare($query);
    $result -> execute();
    $pagos = $result -> fetchAll();

?>
