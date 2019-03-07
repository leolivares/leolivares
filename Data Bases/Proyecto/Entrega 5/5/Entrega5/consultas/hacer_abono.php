<?php

	include_once "includes/psql-config.php";
  	try {
    	$db_bank = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
    	$db_store = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    	echo $e->getMessage();
    }

    $id_usuario = $_SESSION['user_id'];

    $card_id = $_POST['card_id'];
    $monto = $_POST['monto'];

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

    $date = date("Y-m-d");
    $sql_t = "INSERT INTO abonos VALUES (default, '$card_id', '$monto', '$date', '$nebclp');"; 
    $make = $db_bank -> prepare($sql_t);
    $make -> execute();
    $result = $make -> fetchAll();
    

?>