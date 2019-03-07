<?php include 'includes/header.php'; ?>

<?php
if (!isset($_SESSION['user_id'])) {
header("Location: index.php");
exit();
}
?>

<?php 
	
	$must = explode('-', $_GET['must']);
	$must = '1'.implode('-1', $must);


	$could = '';
	if (!empty($_GET['could'])) {
		$could = explode('-', $_GET['could']);
		$could = '-2'.implode('-2', $could);
	}

	$dont = '';
	if (!empty($_GET['dont'])) {
		$dont = explode('-', $_GET['dont']);
		$dont = '-3'.implode('-3', $dont);
	}

	$url = "http://rapanui8.ing.puc.cl/search_text/".$_GET['user'].'/'.$must.$could.$dont;

	$response = file_get_contents($url);
	$data = json_decode($response, true);
	
?>

<div class='container'  style='margin-top: 5%'>
  <div class="row h-100 justify-content-center align-items-center">
    <div class="card text-white bg-secondary mb-3" style="width:70%;">
      <div class="card-header">
            <h3>Messages</h3>

      </div>
    
      <div  class="card-body">

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
							    	foreach ($data as $msg) {

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
        

      </div>
    </div>
  </div>
</div>