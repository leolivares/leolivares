<?php include 'includes/header.php'; ?>

<?php
	if (!isset($_SESSION['user_id'])) {
	header("Location: index.php");
	exit();
	}
?>


<?php
	$user_id = $_SESSION['user_id'];
	$response = file_get_contents("http://rapanui8.ing.puc.cl/user_info/".$user_id);
	$data = json_decode($response, true);
?>



<style>
    #map{ height: 390px; }
  </style>

<div class="container" style="margin-top: 5%;">


	<div class="row h-100 justify-content-center align-items-center">

		<div class="col-sm-8">
			<div class="card text-white bg-secondary mb-3" >
				<div class="card-header">
					<div class="row">
						<div class="col">
							<h4 class="card-title">Messages</h4>
						</div>
					</div>
				</div>

					<div class="card-body">

					<ul class="nav nav-tabs">
						  <li class="nav-item">
						    <a class="nav-link active" data-toggle="tab" href="#sent">Sent</a>
						  </li>
						  <li class="nav-item">
						    <a class="nav-link" data-toggle="tab" href="#received">Received</a>
						  </li>
						</ul>
						<div id="myTabContent" class="tab-content">
						  <div class="tab-pane fade show active" id="sent">
						  	<table class="table table-hover" id="card_table">
								<thead>
								  <tr class='table-info'>
								    <th scope="col">To</th>
								    <th scope="col">Message</th>
								    <th scope="col">Date</th>
								  </tr>
								</thead>
								<tbody>
							    <?php
							    	foreach ($data['messages_sent'] as $msg) {

							    			$response2 = file_get_contents("http://rapanui8.ing.puc.cl/user_info/".$msg['receptant']);
											$data2 = json_decode($response2, true);
							    			echo "<tr class='table-primary'>
										      <td>".$data2['correo']."</td>
										      <td>".$msg['message']."</td>
										      <td>".$msg['date']."</td>
										    </tr>";
							    	};
							    ?>
							</tbody>
						</table>

							<form action="new_message.php">
	    						<input class="btn btn-primary btn-sm" type="submit" value="New Message" />
							</form>


						  </div>
						  <div class="tab-pane fade" id="received">
						    <table class="table table-hover">
								<thead>
								  <tr class='table-info'>
								    <th scope="col">From</th>
								    <th scope="col">Message</th>
								    <th scope="col">Date</th>
								  </tr>
								</thead>
								<tbody>
							    <?php
							    	foreach ($data['messages_received'] as $msg) {
							    		$response4 = file_get_contents("http://rapanui8.ing.puc.cl/user_info/".$msg['sender']);
							    		$data4 = json_decode($response4, true);
							    		echo "<tr class='table-primary'>
										      <td>".$data4['correo']."</td>
										      <td>".$msg['message']."</td>
										      <td>".$msg['date']."</td>
										    </tr>";
							    	};
							    ?>
							</tbody>
						</table>

						  </div>
						</div>

				</div>
			</div>

					<div class="jumbotron">
						<h1 class="display-6">Locations!</h1>
						<div id="map"></div>
						<br>
						<form method="get" action="messages.php" name="form">  

							<div class="row">

								<div class="col">
						            <div class="form-group">
						                  <label class="form-control-label" >From</label>
						                  <input type="date" class="form-control" name="from" required>
						            </div>
						        </div>


						        <div class="col">
							          <div class="form-group">
							          	<label class="form-control-label">To</label>
							          	<input type="date" class="form-control" name='to' id='to' required>
							         </div>
							      </div>
						     

							   <div class="col">
					          <div class="form-group">
					            	<label class="form-control-label">  . </label>
					            	<br>
					              <button type="submit" class="btn btn-primary">Search!</button> 
					          </div>
					      </div>
					        </form>

					        </div>
					</div>

		</div>
		<div class="col-sm-4">
			<div class="card text-white bg-secondary mb-3">
				<div class="card-header">
					<div class="row">
						<div class="col">
							<h4 class="card-title">Search</h4>
						</div>
					</div>
				</div>

					<div class="card-body">

						<form method="get" action="search_text.php">  

					            <div class="form-group">
					                  <label class="form-control-label" >Must have (phrases or words):</label>
					                  <input type="text" class="form-control" min=0 name="must" placeholder="a phrase-word" required>
					            </div>


						          <div class="form-group">
						          	<label class="form-control-label" >Could Have (words):</label>
						          	<input type="text" class="form-control" name='could' placeholder="word1-word2">
						         </div>


						          <div class="form-group">
						          	<label class="form-control-label" >Don't Have (words):</label>
						          	<input type="text" class="form-control" name='dont' placeholder="word1-word2">
						          </div>

					          	<div class="form-group">
						          	<label class="form-control-label" >User (-1 for all DB):</label>
						          	<input type="number" class="form-control" value='-1' min=-1 name='user'>
						         </div>



					          <fieldset>
					            <div class="row h-100 justify-content-center align-items-center">
					              <button type="submit" class="btn btn-primary">Search!</button> 
					            </div>
					          </fieldset>
					        </form>

						  	


				</div>
			</div>
		</div>
	</div>

</div>


	<script>
    var mymap = L.map('map').setView([40.737, -73.923], 1);



	var to = <?php echo (!empty($_GET['to']) ? json_encode($_GET['to']) : '""'); ?>;
	var from = <?php echo (!empty($_GET['from']) ? json_encode($_GET['from']) : '""'); ?>;


	if (to != "") {
		to = Date.parse(to);
		from = Date.parse(from);
	}

   L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibGVvbGl2YXJlcyIsImEiOiJjam93NXN0NnAxc3hqM3ZqeGd3Z2R4ODZkIn0._AXVJtJX7784EjYPaQP-vQ', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibGVvbGl2YXJlcyIsImEiOiJjam93NXN0NnAxc3hqM3ZqeGd3Z2R4ODZkIn0._AXVJtJX7784EjYPaQP-vQ'
}).addTo(mymap);

   var data3 = <?php echo JSON_encode($data['messages_sent']); ?>;

   if (to != "") {
	   	for (var i = 0; i < data3.length; i++)
	    {
	    	var date = Date.parse(data3[i].date);
	    	if (date >= from && date <= to) {
	    		var marker = L.marker([data3[i].lat, data3[i].long]).addTo(mymap);
	        	marker.bindPopup(data3[i].message).openPopup();
	    	}
	    }
   }

   else {
	   	for (var i = 0; i < data3.length; i++)
	    {
	    	var marker = L.marker([data3[i].lat, data3[i].long]).addTo(mymap);
	        marker.bindPopup(data3[i].message).openPopup();
	        
	    }
   }

   


</script>



</div>