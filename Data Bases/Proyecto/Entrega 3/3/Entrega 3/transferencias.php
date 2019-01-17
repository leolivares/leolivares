<?php include 'includes/header.php'; ?>

<?php
  if (!isset($_SESSION['user_id'])) {
  header("Location: index.php");
  exit();
  }
?>

<?php include 'consultas/consulta_saldo.php' ?>

<?php
  if (isset($_POST['make_t'])) {
    if ($saldo > 0 && $saldo >= $_POST['monto']) {
      $error = False;
      include 'consultas/make_transferece.php';
    }
    else {
      $error = True;
      $msg = "Insufficient Balance";
    }
  }
?>



<div class='container'  style='margin-top: 5%'>
  <div class="row h-100 justify-content-center align-items-center">
    <div class="card text-white bg-secondary mb-3" style="width:50%;">
      <div class="card-header">
            <h3>Transferencias</h3>
            <?php
              echo "Tu saldo es $saldo NBC";
            ?>
      </div>
    
      <div  class="card-body">
        <form method="post" action="transferencias.php">  

          <?php
            if (isset($no_user) && $no_user) {
              echo '<div class="form-group has-danger">
                  <label class="form-control-label" for="email">Email Destinatario:</label>
                  <input type="email" class="form-control is-invalid" id="inputInvalid" name="email" placeholder="Ingrese email de usuario a transferir" required>
                  <div class="invalid-feedback">Sorry, that user does not exists. Try another?</div>
                </div>';
            }
            else {
              echo '<div class="form-group">
                  <label class="form-control-label" >Email Destinatario:</label>
                  <input type="email" class="form-control" name="email" placeholder="Ingrese email de usuario a transferir" required>
                </div>';
            }
            ?>
          <div class="form-group">
            <?php
            if (isset($msg)) {
              echo '<div class="form-group has-danger">
                  <label class="form-control-label" for="email">Monto:</label>
                  <input type="number" class="form-control is-invalid" id="inputInvalid" min=0 name="monto" placeholder="Ingrese monto a transferir" required>
                  <div class="invalid-feedback">'.$msg.'</div>
                </div>';
            }
            else {
              echo '<div class="form-group">
                  <label class="form-control-label" >Monto:</label>
                  <input type="number" class="form-control" min=0 name="monto" placeholder="Ingrese monto a transferir" required>
                </div>';
            }

            ?>

          </div>
          <input type='hidden' name='make_t' value='1'>
          <fieldset>
            <div class="row h-100 justify-content-center align-items-center">
              <button type="submit" class="btn btn-primary">Done!</button> 
            </div>
          </fieldset>
        </form>

      </div>
    </div>
  </div>
</div>
  
</div>