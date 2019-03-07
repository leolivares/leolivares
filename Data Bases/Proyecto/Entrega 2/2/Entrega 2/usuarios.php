<?php include 'header.php';?>
<title>Usuarios - NebBank</title>
<?php
  include_once "psql-config.php";
  try {
    $db = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }
 	$query = "SELECT * FROM usuarios ORDER BY id_usuario;";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$usuarios = $result -> fetchAll();
	echo "<br><div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID</th><th scope='col'>Nombre</th><th scope='col'>Apellido</th><th scope='col'>Correo</th><th scope='col'>Sexo</th></tr></thead><tbody>";
	foreach ($usuarios as $usuario) {
  		echo "<tr class='table-secondary'><td>$usuario[0]</td><td>$usuario[1]</td><td>$usuario[2]</td><td>$usuario[3]</td><td>$usuario[4]</td></tr>";;
	}
	echo "</tbody></table></div>";
?>

<form action="index.php" method="post">
  <button type="submit" class="btn btn-primary">Volver</button>
</form>
</div> 
</body>
</html>