

<?php
  include_once "includes/psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    
    $id_tienda = $_GET["tsid"];

    // CONSULTA ARROJA NOMBRE Y CANTIDAD DE VECES VENDIDO DE CADA SERVICIO,
    // EN ORDEN DEL MAS VENDIDO AL MENOS VENDIDO
    $query = "SELECT s.nombre, COUNT(*)
          FROM compraservicio c, servicios s, rcompraservicio r
          WHERE c.id_tienda_s = '$id_tienda'
          AND c.id_compraservicio = r.id_compraservicio
          AND r.id_servicio = s.id_servicio
          GROUP BY s.id_Servicio
          ORDER BY COUNT(*) DESC;";

    $result = $db -> prepare($query);
    $result -> execute();
    $servicios = $result -> fetchAll();

?>
