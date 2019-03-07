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

    if (isset($_GET["sid"])){
      $id_seguro = $_GET["sid"];
      $uid = $_SESSION['user_id'];
      $today = (string)date("Y-m-d");
      $end = (string)date('Y-m-d', strtotime('+1 years'));
      $query = "INSERT INTO usuarioseguro VALUES ($uid, $id_seguro, '$today', '$end');";
      echo $query;
      $add_seguro = $db-> prepare($query);
      $add_seguro -> execute();
    }

    // initialize CURL:
    $apikey = '594833F9-392F-4EA3-B36E-EDC07488649E';
    $ch = curl_init('https://rest.coinapi.io/v1/exchangerate/ETH/USD?apikey='.$apikey);   
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    // get the JSON data:
    $json = curl_exec($ch);
    curl_close($ch);

    // Decode JSON response:
    $resp = json_decode($json, true);

    // access the conversion result
    $ethprice = $resp['rate'];

    // initialize CURL:
    $ch = curl_init('https://free.currencyconverterapi.com/api/v6/convert?q=USD_CLP');   
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    // get the JSON data:
    $json = curl_exec($ch);
    curl_close($ch);

    // Decode JSON response:
    $conversionResult = json_decode($json, true);

    // access the conversion result
    $usdclp = $conversionResult['results']['USD_CLP']['val'];
    $nebclp = round(0.001 * $ethprice * $usdclp);

    $uid = $_SESSION['user_id'];
    $sql_seguros = "SELECT * 
                    FROM seguros 
                    WHERE id_seguro NOT IN (
                      SELECT id_seguro
                      FROM usuarioseguro
                      WHERE id_usuario = $uid);";
    $get_seguros = $db-> prepare($sql_seguros);
    $get_seguros -> execute();
    $seguros = $get_seguros -> fetchAll();

    echo "<div class='container' style='margin-top: 5%'>";
    echo "<h3> Nebcoin: $nebclp CLP</h3>";
    echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID Seguro</th><th scope='col'>Nombre</th><th scope='col'>Descripción</th><th scope='col'>Valor Mensual</th></tr><th> </th></thead><tbody>";
    foreach ($seguros as $seguro) {
      $val = $seguro[3] * $nebclp;
      echo "<tr class='table-secondary'><td>$seguro[0]</td><td>$seguro[1]</td><td>$seguro[2]</td><td>$val CLP</td><td><a href='abonos_seguros.php?sid=$seguro[0]'>Contratar</a></td></tr>";
    }
    echo "</tbody></table>";
    echo "<div>";

?>