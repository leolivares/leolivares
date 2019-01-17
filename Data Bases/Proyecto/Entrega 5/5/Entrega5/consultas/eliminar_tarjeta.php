<?php
	if (isset($_POST['card_id'])) {

	  include_once "includes/psql-config.php";

	  try {
	    $db = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
	    }
	    catch(PDOException $e) {
	    echo $e->getMessage();
	    }

	    $card_id = $_POST['card_id'];

	    $query = "UPDATE tarjetas
	            SET active = 'f'
	            WHERE id_tarjeta = $card_id;";

	    $result = $db -> prepare($query);
	    $result -> execute();

	}


?>