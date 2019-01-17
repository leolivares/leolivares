<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php
	include 'consultas/consulta_search_servicios.php';
?>

<!-- https://bootswatch.com/slate/  -->
<div class="container" style="margin-top: 5%;">


	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-secondary mb-3" style="width:80%;">
			<div class="card-header">
				<h4>Products</h4>
			</div>

			<div class="card-body">
				<table class="table table-hover">
				  <thead>
				    <tr class="table-info">
				      <th scope="col">Service Name</th>
	      			  <th scope="col">Price</th>
				    </tr>
				  </thead>

				<tbody>

				<?php
					foreach ($servicios as $service) {
						echo '<tr class="table-primary">
						      <td><a href="service.php?sid='.$service[0].'">'.$service[1].'</a></td>
						      <td>'.$service[2].'</td>
						    </tr>';
					}

				?>

				 </tbody>
			 </table>
			</div>
		</div>
	</div>

</div>
