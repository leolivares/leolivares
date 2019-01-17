<?php include 'includes/header.php'; ?>

<?php
if (!isset($_SESSION['user_id'])) {
header("Location: index.php");
exit();
}
?>


<?php
  if (isset($_POST['make_t'])) {
  	include 'consultas/check_for_user.php';

  	if (!isset($no_user)) {
  		$url = 'http://rapanui8.ing.puc.cl/new_message';
		$data = array('message' => $_POST['content'], 'sender' => $_SESSION['user_id'], 'receptant' => $r_id, 'lat' => $_POST['lat'], 'long'=> $_POST['long']);

		$options = array(
	    	'http' => array(
	        'header'  => "Content-type: application/json\r\n",
	        'method'  => 'POST',
	        'content' => json_encode($data)
		    )
		);

		$context  = stream_context_create($options);
		$result = file_get_contents($url, false, $context);

		echo '<div class="container"  style="margin-top: 5% ">
  <div class="row h-100 justify-content-center align-items-center"><div class="alert alert-dismissible alert-success" style="width: 50%;">
  			<button type="button" class="close" data-dismiss="alert">&times;</button>
  			<strong>Well done!</strong> Message Sent!.
			</div></div></div>';
  	}
  	else {
  		echo '<div class="container"  style="margin-top: 5%">
  <div class="row h-100 justify-content-center align-items-center"><div class="alert alert-dismissible alert-danger" style="width: 50%;">
  		<button type="button" class="close" data-dismiss="alert">&times;</button>
  		<strong>Oh snap!</strong> <a href="#" class="alert-link">Change a few things up</a> and try submitting again.
			</div></div></div>';
  	}
  }
?>


<div class='container'  style='margin-top: 5%'>
  <div class="row h-100 justify-content-center align-items-center">
    <div class="card text-white bg-secondary mb-3" style="width:50%;">
      <div class="card-header">
            <h3>New Message</h3>
      </div>
    
      <div  class="card-body">
        <form method="post" action="new_message.php">  

          <?php
            if (isset($no_user) && $no_user) {
              echo '<div class="form-group has-danger">
                  <label class="form-control-label" for="email">Email Destinatario:</label>
                  <input type="email" class="form-control is-invalid" id="inputInvalid" name="mail" placeholder="Ingrese email del usuario" required>
                  <div class="invalid-feedback">Sorry, that user does not exists. Try another?</div>
                </div>';
            }
            else {
              echo '<div class="form-group">
                  <label class="form-control-label" >To:</label>
                  <input type="email" class="form-control" name="mail" placeholder="Ingrese email del usuario" required>
                </div>';
            }
            ?>
          <div class="form-group">
            <div class="form-group">
                  <label class="form-control-label" >Message:</label>
                  <input type="text" class="form-control" min=0 name="content" placeholder="Contenido del Mensaje" required>
            </div>

          </div>

          <div class="row h-100 justify-content-center ">

          	<div class="col">
	          <div class="form-group">
	          	<label class="form-control-label" >Latitude:</label>
	          	<input type="number" class="form-control" name='lat' min=-90 max=90 required>
	          </div>
	         </div>

	        <div class="col">

	          <div class="form-group">
	          	<label class="form-control-label" >Longitude:</label>
	          	<input type="number" class="form-control" name='long' min=-180 max=180 required>
	          </div>
	        </div>
	    </div>

          <input type='hidden' name='make_t' value='1'>
          <fieldset>
            <div class="row h-100 justify-content-center align-items-center">
              <button type="submit" class="btn btn-primary">Send!</button> 
            </div>
          </fieldset>
        </form>

      </div>
    </div>
  </div>
</div>