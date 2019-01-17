<!DOCTYPE html>
<html>
<style>
table, th, td {
    border: 1px solid black;
}
</style>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://bootswatch.com/4/slate/bootstrap.min.css">
<link rel="stylesheet" type="text/css" href="custom.css">
<link rel="icon" href="coin.png">

<nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
  <a class="navbar-brand" href="index.php">NebBank <img src="coin.png" style="max-width:32px;"></a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarColor01">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="index.php">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="usuarios.php">Usuarios</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="seguros.php">Seguros</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="tarjetas.php">Tarjetas</a>
      </li>
      <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" id="tables">Otros<span class="caret"></span></a>
              <div class="dropdown-menu" aria-labelledby="Tables">
                <a class="dropdown-item" href="abonos.php">Abonos</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="cuotas.php">Cuotas</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="transacciones.php">Transacciones</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="tarjeta_usuario.php">Tarjetas - Usuarios</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="seguro_usuario.php">Usuarios - Seguros</a>
              </div>
            </li>
        </ul>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="text" placeholder="Search">
      <button class="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>
</head>
<body class="pt-5">