<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php 
	include 'consultas/consulta_compra_detallada.php';
?>

<div class="container" style="margin-top: 5%;">
	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-secondary mb-3" style="width: 70%;">
		  <div class="card-header"><h3>Order #<?php echo $compra_p[0][0]; ?></h3></div>
		  <div class="card-body">
		    <h5 class="card-title"> Order Summary</h5>
		    <table class="table table-hover">
			  <thead>
			  	<?php 
			  	if ($product) {
			  		echo '<tr class="table-info">
					      <th scope="col">Product</th>
					      <th scope="col">Qty</th>
					      <th scope="col">Unit Price</th>
					      <th scope="col">Total</th>
					    </tr>';
			  	}
			  	else {
			  		echo '<tr class="table-info">
					      <th scope="col">Service</th>
					      <th scope="col">Total</th>
					    </tr>';
			  	}
			  	?>

			  </thead>
			  <tbody>
			  	<?php
				  	if ($product) {
				  		foreach ($compra_p as $key) {
					  		echo '<tr class="table-primary">
						      <td>'.$key[4].'</td>
						      <td>'.$key[7].'</td>
						      <td>'.$key[5].'</td>
						      <td>'.$key[8].'</td>
						      </tr>';
				  		}
				  	}
				  	else {
				  		foreach ($compra_s as $key) {
					  		echo '<tr class="table-primary">
						      <td>'.$key[1].'</td>
						      <td>'.$key[3].'</td>
						      </tr>';
				  		}
				  	}
				?>


			</tbody>
		</table>

		Order Total: <?php echo $total; ?> NBC
			    
		  </div>
		</div>
	</div>

	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-secondary mb-3" style="width:70%;">
		  <div class="card-body">
		    <h5 class="card-title">Order Payment</h5>
		    
		    <table class="table table-hover" id="card_table">
			    <thead>
			    	<?php
				    	if ($direct) {
				    	 	echo '<tr class="table-info">
							      	<th scope="col">Paid To</th>        
							        <th scope="col">NBCs</th>
							        <th scope="col">Date</th>
							      </tr>';
				    	 }
				    	 else {
				    	 	echo '<tr class="table-info">
							      	<th scope="col">Paid To</th>        
							        <th scope="col">NBCs</th>
							        <th scope="col">Expiration Date</th>
							        <th scope="col">Paid</th>
							      </tr>';
				    	 } 
			    	
			    	?>
			    </thead>

			    <tbody>
			    	<?php
				    	if ($direct) {
				    	 	foreach ($directs as $dir) {
				    	 		echo "hola";
					    		echo '<tr class="table-primary">
					    			  	<td>'.$compra_p[0][0].'</td>
					    			  	<td>'.$dir[3].'</td>
					    			  	<td>'.$dir[4].'</td>
					    			  </tr>';
				    		}
				    	 }
				    	 else {
				    	 	foreach ($cuotas as $cuo) {
				    	 		$paid = "Yes";
				    	 		if ($cuo[2] == 0) {
				    	 			$paid = "No";
				    	 		}
					    		echo '<tr class="table-primary">
					    			  	<td>'.$compra_p[0][3].'</td>
					    			  	<td>'.$cuo[1].'</td>
					    			  	<td>'.$cuo[0].'</td>
					    			  	<td>'.$paid.'</td>
					    			  </tr>';
					    		}
				    	 } 
			    	
			    	?>


			    </tbody>

		    </table>



		  </div>
		</div>
	</div>


</div>