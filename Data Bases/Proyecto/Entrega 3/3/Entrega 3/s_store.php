<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php
	include 'consultas/consulta_tiendadeservicios.php';
	include 'consultas/consulta_rserviciotienda.php';
	include 'consultas/consulta_saldo.php';
?>


<div class="container" style="margin-top: 5%;">

	<?php
		if (isset($_POST['buy'])) {
			if ($saldo >= ($_POST['price'])) {
				include 'consultas/realizar_compra.php';
				$error = False;
				echo '<div class="row h-100 justify-content-center align-items-center"><div class="alert alert-dismissible alert-success" style="width: 80%;">
	  			<button type="button" class="close" data-dismiss="alert">&times;</button>
	  			<strong>Well done!</strong> your transaction was succesfully done!.
				</div></div>';
			}
			else {
				$error = True;
				echo '<div class="row h-100 justify-content-center align-items-center"><div class="alert alert-dismissible alert-danger" style="width: 80%;">
	  		<button type="button" class="close" data-dismiss="alert">&times;</button>
	  		<strong>Oh snap!</strong> <a href="#" class="alert-link">Change a few things up</a> and try submitting again.
				</div></div>';
			}
		}
	?>


	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-primary mb-3" style="width: 80%;">
		  <div class="card-header"><h4><?php echo $s_store[1]  ?></h4></div>
		  <div class="card-body">
		    <h4 class="card-title">Description</h4>
					<div class="list-group">
						<a class="list-group-item list-group-item-action disabled">
							Category: <?php echo $s_store[6]  ?>
					  </a>
						<a class="list-group-item list-group-item-action disabled">
							Opening: <?php echo $s_store[4]  ?>
					  </a>
						<a class="list-group-item list-group-item-action disabled">
							Closing: <?php echo $s_store[5]  ?>
					  </a>
					  <a  class="list-group-item list-group-item-action active">
					    Address: <?php echo $s_store[2]  ?>
					  </a>
					  <a href="#" class="list-group-item list-group-item-action">
							Phone: <?php echo $s_store[3]  ?>
					  </a>
						<a href="#" class="list-group-item list-group-item-action">
							Mail: <?php echo $s_store[7]  ?>
					  </a>
					</div>


		    <p class="card-text"> </p>
		  </div>
		</div>
	</div>


	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-secondary mb-3" style="width: 80%;">
			<div class="card-header"> <h4>Our Services</h4></div>
			<div class="card-body">

				<table class="table table-hover">
				  <thead>
				    <tr class="table-info">
				      <th scope="col">Service Name</th>
				      <th scope="col">Price</th>
					  <th scope="col">Dues</th>
					  <th scope="col">Buy Now!</th>
				    </tr>
				  </thead>

				<tbody>

				<?php
					foreach ($rservicios as $servicio) {
						echo '<tr class="table-primary">
						      <td><a href="s_store.php?tsid='.$s_store[0].'">'.$servicio[1].'</a></td>
						      <td>'.$servicio[2].' NBC</td>
									<form action="s_store.php?tsid='.$s_store[0].'" method="post">
										<input type="hidden" name="buy" value=1>
										<input type="hidden" name="servicio_id" value="'.$servicio[0].'">
										<input type="hidden" name="price" value="'.$servicio[2].'">

										<td>
										<div class="row h-100 justify-content-center align-items-center">
										<input type="number" class="form-control" min="0" value="0" name="dues" style="width: 45%;" require>
										</div>
										</td>

										<td>
											<button type="Submit" class="btn btn-primary btn-sm">Buy</button>
										</td>
									</form>
							    </tr>';
					}

				?>

				 </tbody>
			 </table>
			</div>
		</div>
	</div>
</div>
