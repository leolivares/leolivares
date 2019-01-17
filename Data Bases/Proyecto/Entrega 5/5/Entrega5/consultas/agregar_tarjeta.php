<?php
	if (isset($_POST['add_card'])) {

	  include_once "includes/psql-config.php";

	  try {
	    $db = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
	    }
	    catch(PDOException $e) {
	    echo $e->getMessage();
	    }

	    $user_id = $_SESSION['user_id'];
	    $card_id = $_POST['card_number'];
	    $cvv = $_POST['card_cvv'];
	    $date = $_POST['exp_date'];

	    $query = "INSERT INTO tarjetas VALUES ('$card_id', '$user_id', '$cvv', '$date', 't');";

	    $result = $db -> prepare($query);
	    $result -> execute();

	}


?>