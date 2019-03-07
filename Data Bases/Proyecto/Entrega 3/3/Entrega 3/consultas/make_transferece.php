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

    $email = $_POST['email'];
    $monto = $_POST['monto'];

    $sql = "SELECT * FROM usuarios WHERE usuarios.correo = '$email'"; 


	$get_user = $db_bank -> prepare($sql);
	$get_user -> execute();
	$user = $get_user -> fetchAll();

    if (empty($user)) {
        $no_user = True;
    }
    else {
        $no_user = False;
        $user = $user[0][0];
        $date = date("Y-m-d");
        $sql_t = "INSERT INTO transferencias VALUES (default, '$id_usuario', '$user', '$monto', '$date');"; 
        $make = $db_bank -> prepare($sql_t);
        $make -> execute();
        $result = $make -> fetchAll();
    }




?>