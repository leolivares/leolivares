<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php
	include 'consultas/agregar_tarjeta.php';
	include 'consultas/eliminar_tarjeta.php';
	include 'consultas/consulta_saldo.php';
	include 'consultas/consulta_tarjetas.php';
	include 'consultas/consulta_seguros.php';
	include 'consultas/consulta_compras.php';
?>


<div class="container" style="margin-top: 5%;">

	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-secondary mb-3" style="width:80%;">
			<div class="card-header">
				<div class="row">
					<div class="col">
						<?php
						echo $_SESSION['email'].'</div><div class="col"> Balance: '.$saldo.' NBC</div></div></div>
						<div class="card-body">
						  <h4 class="card-title">User Information</h4>'
						?>

				<ul class="nav nav-tabs">
					  <li class="nav-item">
					    <a class="nav-link active" data-toggle="tab" href="#cards">Credit Cards</a>
					  </li>
					  <li class="nav-item">
					    <a class="nav-link" data-toggle="tab" href="#seguros">Insurances</a>
					  </li>
					</ul>
					<div id="myTabContent" class="tab-content">
					  <div class="tab-pane fade show active" id="cards">
					  	<table class="table table-hover" id="card_table">
							<thead>
							  <tr class='table-info'>
							    <th scope="col">Card Number</th>
							    <th scope="col">CVV</th>
							    <th scope="col">Expiration Date</th>
							    <th scope="col"></th>
							  </tr>
							</thead>
							<tbody>
						    <?php
						    	foreach ($cards as $card) {
						    		if ($card[4] == 't') {
						    			echo "<tr class='table-primary'>
									      <th scope='row'>$card[0]</th>
									      <td>$card[2]</td>
									      <td>$card[3]</td>
									      <td><form action='profile.php' method='post'> <input type='hidden' name='card_id' value=$card[0]><button type='submit' class='btn btn-primary btn-sm'>Remove</button></form></td>
									    </tr>";
						    		}
						    	}
						    ?>
						</tbody>
					</table>

					<form action='profile.php' method='post'>
						<div class="row h-100 justify-content-center align-items-center">
							<input type='hidden' name='add_card' value='1'>
							<input type="number" class="form-control" name="card_number" placeholder="Enter Card Number" style="width: 20%;" required>
							<input type="number" class="form-control" name="card_cvv" placeholder="Enter CVV" style="width: 20%;" required>
							<input type="date" class="form-control" name="exp_date" style="width: 20%;" required>

							<button type="Submit" class="btn btn-primary btn-sm">Add Credit Card</button>
						</div>
					</form>



					  </div>
					  <div class="tab-pane fade" id="seguros">
					    <table class="table table-hover">
							<thead>
							  <tr class='table-info'>
							    <th scope="col">Name</th>
							    <th scope="col">Since</th>
							    <th scope="col">Expiration Date</th>
							  </tr>
							</thead>
							<tbody>
						    <?php
						    	foreach ($seguros as $seguro) {
						    		echo '<tr class="table-primary">
									      <td>'.$seguro[1].'</td>
									      <td>'.$seguro[6].'</td>
									      <td>'.$seguro[7].'</td>
									    </tr>';
						    	}
						    ?>
						</tbody>
					</table>
					<form action="abonos_seguros.php">
    					<input class="btn btn-primary btn-sm" type="submit" value="Add Insurance" />
						</form>
					  </div>
					</div>

			</div>
		</div>
	</div>

	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-secondary mb-3" style="width:80%;">
		  <div class="card-body">
		    <h4 class="card-title">Orders</h4>

		    <table class="table table-hover" id="card_table">
			    <thead>
			      <tr class='table-info'>
			      	<th scope="col">Paid To</th>
			        <th scope="col">NBCs</th>
			        <th scope="col">Date</th>
			        <th scope="col"></th>
			      </tr>
			    </thead>

			    <tbody>
			    	<?php

			    	foreach ($compra_p as $cp) {
			    		echo '<tr class="table-primary">
			    			  	<td>'.$cp[2].'</td>
			    			  	<td>'.$cp[3].'</td>
			    			  	<td>'.$cp[4].'</td>
			    			  	<td><form action="order.php" method="get">
			    			  		<input type="hidden" name="c_id" value="'.$cp[0].'">
			    			  		<button type="submit" class="btn btn-primary btn-sm">Check</button>
			    			  		</form>
			    			  	</td>
			    			  </tr>';
			    	}

			    	foreach ($compra_s as $cs) {
			    		echo '<tr class="table-primary">
			    			  	<td>'.$cs[2].'</td>
			    			  	<td>'.$cs[3].'</td>
			    			  	<td>'.$cs[4].'</td>
			    			  	<td><form action="order.php" method="get">
			    			  		<input type="hidden" name="c_id" value="'.$cs[0].'">
			    			  		<button type="submit" class="btn btn-primary btn-sm">Check</button>
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
