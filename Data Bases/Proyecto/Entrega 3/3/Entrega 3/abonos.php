<?php include 'includes/header.php'; ?>

<?php
if (!isset($_SESSION['user_id'])) {
header("Location: index.php");
exit();
}
?>

<?php
    include_once "includes/psql-config.php";
    try {
        $db = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
    }
    catch(PDOException $e) {
      echo $e->getMessage();
    }
    include "consultas/consulta_tarjetas.php";
    if (isset($_POST['make_a'])) {
        include 'consultas/hacer_abono.php';
      }
?>

<div class="container" style="margin-top: 5%">
<table class="table table-hover" id="card_table">
    <thead>
        <tr class='table-info'>
        <th scope="col">Card Number</th>
        <th scope="col">CVV</th>
        <th scope="col">Expiration Date</th>
        <th scope="col">Abonar a la cuenta</th>
        <th scope="col"></th>
        </tr>
    </thead>
    <tbody>
    <?php
        foreach ($cards as $card) {
            if ($card[4] == 't') {
                echo "<tr class='table-primary'>
                    <th scope='row'>$card[0]</th>
                    <td>$card[2]</td>
                    <td>$card[3]</td>
                    <td><form class='form-inline' action='abonos.php' method='post'> <input type='hidden' name='card_id' value=$card[0]> <div class='form-group'>
                    <input type='number' class='form-control-m' min=0 name='monto' placeholder='Ingrese monto' required><input type='hidden' name='make_a' value='1'>
                  </div></td><td><button type='submit' class='btn btn-primary btn-sm'>Abonar</button></form></td>
                </tr>";
            }
        }
    ?>
</div>