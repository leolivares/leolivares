<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php
	include 'consultas/consulta_search_all_stores.php';
?>

<!-- https://bootswatch.com/slate/  -->
<div class="container" style="margin-top: 5%;">

	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-secondary mb-3" style="width:80%;">
			<div class="card-header">
				<h4>Stores</h4>
			</div>
			<div class="card-body">
				<ul class="nav nav-tabs">
					<li class="nav-item">
					    <a class="nav-link active" data-toggle="tab" href="#ps">Product Stores</a>
					  </li>
					  <li class="nav-item">
					    <a class="nav-link" data-toggle="tab" href="#ss">Service Stores</a>
					  </li>
				</ul>
				<div id="myTabContent" class="tab-content">
					  <div class="tab-pane fade show active" id="ps">
					  	<table class="table table-hover">
							  <thead>
							    <tr class="table-info">
							      <th scope="col">Store Name</th>
							      <th scope="col">Category</th>
							    </tr>
							  </thead>

							<tbody>

							<?php

								foreach ($tiendas_productos as $tienda_p) {
									echo '<tr class="table-primary">
									      <td><a href="store.php?tpid='.$tienda_p[2].'">'.$tienda_p[0].'</a></td>
									      <td>'.$tienda_p[1].'</td>
									    </tr>';
								}

							?>

							 </tbody>
						 </table>
					  </div>
				

					  <div class="tab-pane fade" id="ss">
					  	<table class="table table-hover">
						  <thead>
						    <tr class="table-info">
						      <th scope="col">Store Name</th>
						      <th scope="col">Category</th>
						    </tr>
						  </thead>

						<tbody>

						<?php
							foreach ($tiendas_servicios as $tienda_s) {
								echo '<tr class="table-primary">
								      <td><a href="s_store.php?tsid='.$tienda_s[2].'">'.$tienda_s[0].'</a></td>
								      <td>'.$tienda_s[1].'</td>
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


</div>
