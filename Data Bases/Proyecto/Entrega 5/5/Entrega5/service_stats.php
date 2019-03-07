<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
		header("Location: index.php");
		exit();
	}

?>

<?php
	include 'consultas/consultas_stats_1.php';
	include 'consultas/consultas_stats_2.php';
	include 'consultas/consultas_stats_3.php';
?>



<link href="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.css" rel="stylesheet" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.js"></script>

<style type="text/css">
.c3 .c3-axis-x path,
.c3 .c3-axis-x line,
.c3 .c3-axis-y path,
.c3 .c3-axis-y line,
.c3 text.c3-text,
path.domain {
    stroke: white;
}

.c3 .c3-axis-x g,
.c3 .c3-axis-y g,
.c3 .c3-legend-item text,
path.domain {
    fill: white;
}
</style>


<div class="container" style="margin-top: 5%">
	<div class="container" style="margin-top: 5%">
	<div class="row h-100 justify-content-center align-items-center">
		<div class="card text-white bg-secondary mb-3" style="width:80%;">
			<div class="card-header">
				<h3> Top Costumers </h3>
			</div>
			<div class="card-body">
				    <table class="table table-hover">
				      <thead>
				        <tr class="table-info">
				          <th scope="col">User ID</th>
				          <th scope="col">Name</th>
				          <th scope="col">Amount</th>
				        </tr>
				      </thead>

				    <tbody>

				    <?php
				      foreach ($usuarios as $usuario) {
				        echo '<tr class="table-primary">
				              <td>'.$usuario[0].'</td>
				              <td>'.$usuario[1].'</td>
				              <td>'.$usuario[2].' NBC</td>
				            </tr>';
				      }

				    ?>

				     </tbody>
				   </table>
				 </div>

			</div>				 
  		</div>
 	</div>


		<div class="row">
			<div class="col">

				<div class="card text-white bg-secondary mb-3">
					<div class="card-header">
						<h3> Revenue per Month </h3>
					</div>
					<div class="card-body">
						<div id="chart"></div>
					</div>
				</div>


			</div>


			<div class="col">
				<div class="card text-white bg-secondary mb-3">
					<div class="card-header">
						<h3> Products Sold </h3>
					</div>
					<div class="card-body">
						<div id="chart2"></div>
					</div>
				</div>
			</div>

		</div>
</div>

<script>
  var new_array = <?php echo json_encode($pagos)?>;
  var dates = new Array((new_array.length + 1));
  var money = new Array((new_array.length + 1));

  money[0] = "Paymento";


  for (var i = new_array.length-1; i >= 0; i--) { 
	  dates[i] = new_array[i][0].split(" ")[0].split("-").slice(0, 2).reverse().join("-");
	  money[i+1] = new_array[i][1];
  }

  var chart = c3.generate({
		bindto : '#chart',
		data: {
				columns: [
						money
					]
			},

		axis: {
	        x: {
	            type: 'category',
	            categories: dates
	        }
    }

   });




	</script>

<script>
	// Second Chart

	var services = <?php echo json_encode($servicios)?>;
	var x = new Array(services.length);
	for (var i = x.length - 1; i >= 0; i--) { 
	  x[i] = new Array(services[i][0], services[i][1]);
	}
	console.log(x);
	var chart2 = c3.generate({
	bindto : '#chart2',
    data: {
        columns: x,
        type : 'pie'
    }
});




</script>




