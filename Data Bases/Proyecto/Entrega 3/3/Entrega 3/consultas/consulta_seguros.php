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


    $sql_seguros = "SELECT * FROM seguros AS S, usuarioseguro AS R WHERE S.id_seguro = R.id_seguro AND R.id_usuario = '$id_usuario';";
    $get_seguros = $db_bank -> prepare($sql_seguros);
    $get_seguros -> execute();
    $seguros = $get_seguros -> fetchAll();

?>