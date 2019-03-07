<?php include 'header.php';?>
<title>Bienvenido a NebBank</title>
<br>
<div class="container">
  <div class="jumbotron">
  <form action="consulta_fecha.php" method="post">
    <fieldset>
      <div class="form-group">
        <label for="Transacciones realizadas en una fecha">Transacciones realizadas en una fecha</label>
        <input type="date" name="fecha" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Ingrese Fecha">
      </div>
      </fieldset>
      <button type="submit" class="btn btn-primary">Submit</button>
    </fieldset>
  </form>
  </div>
</div>

<div class="container">
<div class="jumbotron">
<form action="consulta_abonos.php" method="get">
  <fieldset>
    <div class="form-group">
      <label for="Abonos realizados">Abonos realizados</label>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
    </fieldset>
  </fieldset>
</form>
</div>
</div>

<div class="container">
<div class="jumbotron">
<form action="consulta_seguros.php" method="get">
  <fieldset>
    <div class="form-group">
      <label for="Seguro más contratado">Seguro más contratado</label>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
    </fieldset>
  </fieldset>
</form>
</div>
</div>

<div class="container">
<div class="jumbotron">
<form action="consulta_mayores_pagos.php" method="get">
  <fieldset>
    <div class="form-group">
      <label for="Usuario con Mayor Cantidad de Dinero Transferido">Usuario con Mayor Cantidad de Dinero Transferido</label>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
    </fieldset>
  </fieldset>
</form>
</div>
</div>

<div class="container">
<div class="jumbotron">
<form action="consulta_por_pagar.php" method="post">
  <fieldset>
    <div class="form-group">
      <label class="col-form-label" for="inputDefault">Monto por pagar según Transaccion</label>
      <input type="number" class="form-control" name="id_pago" placeholder="Ingrese Id de Transaccion por Cuota" id="id_pago">
    </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </fieldset>
  </fieldset>
</form>
</div>
</div>

<div class="container">
<div class="jumbotron">
<form action="consulta_saldo.php" method="post">
  <fieldset>
    <div class="form-group">
      <label for="Saldo actual de usuario">Saldo actual de usuario</label>
      <input type="number" name="id_usuario" class="form-control" placeholder="Ingrese Id de Usuario" id="inputDefault">
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
    </fieldset>
  </fieldset>
</form>


</body>
</html>