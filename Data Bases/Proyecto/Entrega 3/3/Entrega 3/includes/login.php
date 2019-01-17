<?php

	include_once "psql-config.php";
  	try {
    	$db_bank = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
    	$db_store = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    	echo $e->getMessage();
    }

    if (isset($_POST['login'])) {
  
		$email = $_POST['email'];
		$pwd = $_POST['password'];


		$query = "SELECT * FROM usuarios AS U WHERE U.correo = '$email';";
		$result = $db_bank -> prepare($query);
		$result -> execute();
		$user = $result -> fetch();

		if ($user) {
			if ($user[6] == $pwd) {
				session_start();
				$_SESSION['user_id'] = $user[0];
				$_SESSION['nombre'] = $user[1];
				$_SESSION['apellido'] = $user[2];
				$_SESSION['email'] = $user[3];

				header("Location: ../home.php?login=success");
				exit();
			}

			else {
				header("Location: ../index.php?error=invalidpwd");
				exit();
			}
		}
		else {
			header("Location: ../index.php?error=invaliduser");
			exit();
		}

	}

	else {
		header("Location: ../index.php");
		exit();
	}
