<?php

	  include_once "includes/psql-config.php";

	  try {
	    $db = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
	    }
	    catch(PDOException $e) {
	    echo $e->getMessage();
	    }

	    $mail = $_POST['mail'];

	    $query = "SELECT * FROM usuarios WHERE usuarios.correo = '$mail';";

	    $result = $db -> prepare($query);
	    $result -> execute();

	    $user = $result -> fetchAll();

	    if (empty($user)) {
	        $no_user = True;
	    }
	    else {
	    	$r_id = $user[0]['id_usuario'];
	    }



?>