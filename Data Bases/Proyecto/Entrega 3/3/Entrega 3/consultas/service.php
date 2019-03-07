<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php
	include 'consultas/consulta_servicio.php';
	include 'consultas/consulta_rtiendaservicio.php';
?>



<div class="container" style="margin-top: 5%;">
	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-primary mb-3" style="width: 70%;">
		  <div class="card-header">
				<div class="row">
					<div class="col">
						<?php
						echo $service[1].'</div><div class="col"> Precio: '.$service[2].' NBC</div></div></div>
						<div class="card-body">
							<h4 class="card-title">Description</h4>'
						?>

		  <div class="card-body">
		    <p class="card-text"> <?php echo $service[3]  ?></p>
		  </div>
		</div>
	</div>
</div>


<div class="container" style="margin-top: 5%;">
	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-primary mb-3" style="width: 70%;">
			<div class="card-body">
				<h4>Stores</h4>
			</div>

			<table class="table table-hover">
				<thead>
					<tr>
						<th scope="col">Store Name</th>
						<th scope="col">Category</th>
						<th scope="col"></th>
					</tr>
				</thead>

			<tbody>

			<?php
				foreach ($rtiendas as $rtienda) {
					echo '<tr class="table-active">
								<td>'.$rtienda[0].'</td>
								<td>'.$rtienda[1].'</td>
								<td>
								<form class="form-inline my-2 my-lg-0" action="s_store.php" method="get">
									<input type="hidden" name="tsid" value="'.$rtienda[2].'">
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
