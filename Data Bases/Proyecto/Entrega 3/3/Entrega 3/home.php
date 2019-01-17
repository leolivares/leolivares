<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>


<div class="container" style="margin-top: 5%;">

	<div class="row">
		<div class="col">

			<div class="card mb-3">
			  <h3 class="card-header">Stores</h3>
			  <div class="card-body">
			  </div>
			  <div class="row h-100 justify-content-center align-items-center">
			  	<img style="height: 50%; width: 50%; display: block;" src="imgs/store.png" alt="Store image">
			  </div>
			  <div class="card-body">
			    <p class="card-text">Access all the NebStores for different Products and Services!</p>
			  </div>
			  <ul class="list-group list-group-flush">
			    <li class="list-group-item" style="text-align: center;">
			    	<div class="row h-100 justify-content-center align-items-center">
						<form class="form-inline my-2 my-lg-0" action="all_stores.php" method="get">
							<button type="submit" class="btn btn-primary">All Stores</button>
						</form>
					</div>
				</li>

			    <li class="list-group-item">
			    	<form class="form-inline my-2 my-lg-0" action="searched_store.php" method="get">
				      <input type="text" name="nombre_tienda" class="form-control mr-sm-2" placeholder="Search Store">
				      <button class="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
				    </form>
			    </li>
			  </ul>
			  <div class="card-footer text-muted">
			  </div>
			</div>
		</div>

		<div class="col">
			<div class="card mb-3">
			  <h3 class="card-header">Products</h3>
			  <div class="card-body">
			  </div>
			  <div class="row h-100 justify-content-center align-items-center">
			  	<img style="height: 50%; width: 50%; display: block;" src="imgs/cart.png" alt="Cart image">
			  </div>

			  <div class="card-body">
			    <p class="card-text">Take a look at our different available products!</p>
			  </div>
			  <ul class="list-group list-group-flush">
			  	<li class="list-group-item" style="text-align: center;">
			  		<div class="row h-100 justify-content-center align-items-center">
					  	<form class="form-inline my-2 my-lg-0" action="all_products.php" method="get">
					    	<button type="submit" class="btn btn-primary">All Products</button>
					    </form>
					</div>
			    </li>
			    <li class="list-group-item">

			    	<form class="form-inline my-2 my-lg-0" action="searched_product.php" method="get">
				      <input type="text" name="nombre_producto" class="form-control mr-sm-2" placeholder="Search Product">
				      <button class="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
				    </form>
			    </li>
			  </ul>
			  <div class="card-footer text-muted">
			  </div>
			</div>
		</div>

		<div class="col">
			<div class="card mb-3">
			  <h3 class="card-header">Services</h3>
			  <div class="card-body">
			  </div>
			  <div class="row h-100 justify-content-center align-items-center">
			  	<img style="height: 50%; width: 50%; display: block;" src="imgs/customer-service.png" alt="Service image">
			  </div>
			  <div class="card-body">
			    <p class="card-text">Enjoy our variety of services with great deals!</p>
			  </div>



			  <ul class="list-group list-group-flush">
			  	<li class="list-group-item" style="text-align: center;">
						<div class="row h-100 justify-content-center align-items-center">
			  			<form class="form-inline my-2 my-lg-0" action="all_services.php" method="get">
								<button type="submit" class="btn btn-primary">All Services</button>
							</form>
					</div>
					</li>
					<li class="list-group-item">

						<form class="form-inline my-2 my-lg-0" action="searched_service.php" method="get">
				      <input type="text" name="nombre_servicio" class="form-control mr-sm-2" placeholder="Search Service">
				      <button class="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
				    </form>
			    </li>
			  </ul>
			  <div class="card-footer text-muted">
			  </div>
			</div>
		</div>
	</div>
</div>
