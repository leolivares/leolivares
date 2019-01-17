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
 	$query = "SELECT * FROM segurousuario ORDER BY id_usuario;";
	$result = $db -> prepare($query);
	$result -> execute();
	# Ojo, fetch() nos retorna la primer fila, fetchAll()
	# retorna todas.
	$relaciones = $result -> fetchAll();
	echo "<br><div class='container'>";
	echo "<div class='table-responsive'><table class='table table-hover'><thead><tr><th scope='col'>ID Usuario</th><th scope='col'>ID Seguro</th></tr></thead><tbody>";
	setlocale(LC_MONETARY, 'es_CL');
	foreach ($relaciones as $relacion) {
  		echo "<tr class='table-secondary'><td>$relacion[0]</td><td>$relacion[1]</td></tr>";;
	}
	echo "</tbody></table></div>";
?>

<form action="index.php" method="post">
  <button type="submit" class="btn btn-primary">Volver</button>
</form>
</div> 
</body>
</html>