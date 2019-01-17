<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php
	include 'consultas/consulta_producto.php';
	include 'consultas/consulta_rtiendaproducto.php';
?>



<div class="container" style="margin-top: 5%;">
	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-secondary mb-3" style="width: 70%;">
		  <div class="card-header">
				<div class="row">
					<div class="col">
						<?php
						echo $product[1].'</div><div class="col"> Precio: '.$product[3].' NBC</div></div></div>
						<div class="card-body">
							<h4 class="card-title">Description</h4>'
						?>

		  <div class="card-body">
		  	<div class="jumbotron">
		    <p class="card-text"> <?php echo $product[2]  ?></p>
		</div>
		  </div>
		</div>
	</div>
</div>


		<div class="row h-100 justify-content-center align-items-center">
			<div class="card text-white bg-secondary mb-3" style="width: 70%;">
				<div class="card-header">
			    <h4>Stores</h4>
			  </div>

			  <div class="card-body">
				<table class="table table-hover">
				  <thead>
				    <tr class="table-info">
				      <th scope="col">Store Name</th>
				      <th scope="col">Category</th>
							<th scope="col"></th>
				    </tr>
				  </thead>

				<tbody>

				<?php
					foreach ($rtiendas as $rtienda) {
						echo '<tr class="table-primary">
						      <td>'.$rtienda[0].'</td>
						      <td>'.$rtienda[1].'</td>
									<td>
									<form class="form-inline my-2 my-lg-0" action="store.php" method="get">
										<input type="hidden" name="tpid" value="'.$rtienda[2].'">
										<button type="submit" class="btn btn-primary btn-sm">Go to store</button></li>
									</form>
									</td>
						    </tr>';
					}

				?>

				 </tbody>
			 </table>
			</div>
	  </div>
	 </div>
 </div>
</div>
