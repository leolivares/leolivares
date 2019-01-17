<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php
	include 'consultas/consulta_tiendadeproductos.php';
	include 'consultas/consulta_rproductotienda.php';
	include 'consultas/consulta_saldo.php';
?>

<div class="container" style="margin-top: 5%;">

<?php
	if (isset($_POST['buy'])) {

		if ($saldo >= ($_POST['qty'] * $_POST['price'])) {
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
		<div class="card text-white bg-secondary mb-3" style="width: 80%;">
		  <div class="card-header"> <h4><?php echo $store[1]  ?></h4></div>
		  <div class="card-body">
		    <h5 class="card-title">Description</h5>
					<div class="list-group">
						<a class="list-group-item list-group-item-action disabled">
							Category: <?php echo $store[4]  ?>
					  </a>
					  <a  class="list-group-item list-group-item-action active">
					    Address: <?php echo $store[2]  ?>
					  </a>
					  <a href="#" class="list-group-item list-group-item-action">
							Phone: <?php echo $store[3]  ?>
					  </a>
						<a href="#" class="list-group-item list-group-item-action">
							Mail: <?php echo $store[5]  ?>
					  </a>

					</div>


		    <p class="card-text"> </p>
		  </div>
		</div>
	</div>


	<div class="row h-100 justify-content-center align-items-center">

		<div class="card text-white bg-secondary mb-3" style="width: 80%;">
			<div class="card-header"> <h4>Our Products</h4></div>
			<div class="card-body">

				<table class="table table-hover">
				  <thead>
				    <tr class="table-info">
				      <th scope="col">Product Name</th>
				      <th scope="col">Price</th>
					  <th scope="col">Quantity</th>
					  <th scope="col">Dues</th>
					  <th scope="col">Buy Now!</th>
				    </tr>
				  </thead>

				<tbody>

				<?php
					foreach ($rproductos as $producto) {

						echo '<tr class="table-primary">
						      <td><a href="store.php?tpid='.$store[0].'">'.$producto[1].'</a></td>
						      <td>'.$producto[3].' NBC</td>
									<form action="store.php?tpid='.$store[0].'" method="post">
										<td>
										<div class="row h-100 justify-content-center align-items-center">
										<input type="number" class="form-control" min="1" value="1" name="qty" style="width: 45%;" require>
										</div>
										</td>
										<td>
										<div class="row h-100 justify-content-center align-items-center">
										<input type="number" class="form-control" min="0" value="0" name="dues" style="width: 45%;" require>
										</div>
										</td>
										<input type="hidden" name="buy" value=1>

										<input type="hidden" name="product_id" value="'.$producto[0].'">
										<input type="hidden" name="price" value="'.$producto[3].'">

										<td>
			    			  		<button type="submit" class="btn btn-primary btn-sm">Buy</button>
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
