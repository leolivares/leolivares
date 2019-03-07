<?php
  include_once "includes/psql-config.php";
  try {
    $db_bank = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
    // $id_nuevo = $_POST["id_elegido"];
    $id_tienda = $_GET["tpid"];

    // Consulta arroja las fechas agrupadas por mes y el monto total
    // recibido por la tienda en ese mes. 

    $query = "SELECT ALL SUM(monto) as total,
          date_trunc('month', fecha_transaccion)
          AS MES
          FROM (
          SELECT monto, fecha_transaccion
          FROM pagos
          WHERE id_usuario2 = '$id_tienda' AND id_pago in (
          SELECT id_pago
          FROM pagos
          EXCEPT
          SELECT id_pago
          FROM cuotas)
          UNION ALL
          SELECT cuotas.monto AS monto,
          fecha_transaccion
          FROM cuotas, pagos
          WHERE
          cuotas.id_pago = pagos.id_pago
          AND cuotas.pagado = 1
          AND id_usuario2 = '$id_tienda'
          ) as foo
          GROUP BY (MES) ORDER BY (MES);";

    $result = $db_bank -> prepare($query);
    $result -> execute();
    $pagos = $result -> fetchAll();

?>
