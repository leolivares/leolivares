<?php

	include_once "psql-config.php";
  	try {
    	$db_bank = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
    	$db_store = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    	echo $e->getMessage();
    }


	if (isset($_POST['register'])) {
  

		$email = $_POST['email_up'];
		$first_name = $_POST['first_name'];
		$last_name = $_POST['last_name'];
		$sex = $_POST['sex'];
		$age = $_POST['age'];
		$pwd = $_POST['pwd'];
		$pwdrepeat = $_POST['pwd2'];


		if ($pwd != $pwdrepeat) {
			header("Location: ../index.php?error=differentpwds&email=".$email."&fn=".$first_name."&ln=".$last_name);
			exit();
		}
		else if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
			header("Location: ../index.php?error=invalidmail&fn=".$first_name."&ln=".$last_name);
			exit();
		}
		else {

			$query = "SELECT * FROM usuarios AS U WHERE U.correo = '$email';";
			$result = $db_bank -> prepare($query);
			$result -> execute();
			$user = $result -> fetch();


			if ($user) {
				header("Location: ../index.php?error=usertaken&fn=".$first_name."&ln=".$last_name);
				exit();
			}
			else {
				$sql = "INSERT INTO usuarios VALUES (default, '$last_name', '$first_name', '$email', '$sex', '$age', '$pwd');";
				$insert_bank = $db_bank -> prepare($sql);
				$insert_store = $db_store -> prepare($sql);

				$insert_bank -> execute();
				$insert_store -> execute();



				$url = 'http://rapanui8.ing.puc.cl/new_user';
				$data = array('nombre' => $first_name, 'apellido' => $last_name, 'correo' => $email, 'sexo' => $sex, 'edad'=> $age, 'clave'=> $pwd);

				$options = array(
			    	'http' => array(
			        'header'  => "Content-type: application/json\r\n",
			        'method'  => 'POST',
			        'content' => json_encode($data)
				    )
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($url, false, $context);




				header("Location: ../index.php?signup=success");
				exit();

			}
		}
	}

