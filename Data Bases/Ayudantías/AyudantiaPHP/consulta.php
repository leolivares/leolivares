<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>

    <?php

    require("conexion.php"); #Llama a conexión, crea el objeto PDO y obtiene la variable $db

    $edad = $_POST["numero"];
    $query = "SELECT ... WHERE something = '$edad';";
    $result = $db -> prepare($query);
    $result -> execute();
    $dataCollected = $result -> fetchAll(); #Obtiene todos los resultados de la consulta en forma de un arreglo
    #print_r($dataCollected); #si quieren ver el arreglo de la consulta usar print_r($array);
    ?>

    <table><tr> <th>var1</th> <th>var2</th> <th>var3</th> </tr>

    <?php
    foreach ($dataCollected as $p) {
      echo "<tr> <th>$p[0]</th> <th>$p[1]</th> <th>$p[2]</th> </tr>";
    }
    ?>

    </table>


    <form action="index.php" method="post">
      <input type="submit" value="Volver">
    </form>


  </body>
</html>
