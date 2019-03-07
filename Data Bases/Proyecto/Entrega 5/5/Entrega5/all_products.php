<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php
	include 'consultas/consulta_search_all_products.php';
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
				      <th scope="col">Product Name</th>
				      <th scope="col">Price</th>
				    </tr>
				  </thead>

				<tbody>

				<?php
					foreach ($productos as $product) {
						echo '<tr class="table-primary">
						      <td><a href="product.php?pid='.$product[0].'">'.$product[1].'</a></td>
						      <td>'.$product[3].'</td>
						    </tr>';
					}

				?>

				 </tbody>
			 </table>
			</div>
		</div>


	

</div>
