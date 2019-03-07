<?php include 'header.php';?>
<title>Transacciones por Fecha - NebBank</title>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
	 	$fecha = $_POST["fecha"];


    $query = "SELECT P.id_pago, U1.nombre, U1.apellido, U2.nombre, U2.apellido, P.monto FROM pagos AS P, usuarios AS U1, usuarios AS U2 WHERE P.id_usuario1 = U1.id_usuario AND P.id_usuario2 = U2.id_usuario AND P.fecha = '$fecha';";

    $result = $db -> prepare($query);
    $result -> execute();
    $resultados = $result -> fetchAll();
    setlocale(LC_MONETARY, 'es_CL');
    echo "<br>";
    echo "<div class='container'>";
    echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID Pago</th><th scope='col'>Remitente</th><th scope='col'>Destinatario</th><th scope='col'>Cantidad</th></tr></thead><tbody>";
    foreach ($resultados as $fecha) {
      $u1 = $fecha[1] . ' ' . $fecha[2];
      $u2 = $fecha[3] . ' ' . $fecha[4];
      $number = money_format('%.2n', $fecha[5]);
      echo "<tr class='table-secondary'><td>$fecha[0]</td><td>$u1</td><td>$u2</td><td>$number NBC</td></tr>";
    }

    echo "</tbody></table><div>";
?>

<form action="index.php" method="post">
  <button type="submit" class="btn btn-primary">Volver</button>
</form> 
</body>
</html>