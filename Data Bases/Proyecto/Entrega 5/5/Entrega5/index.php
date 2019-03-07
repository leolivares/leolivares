<!DOCTYPE html>
<html>

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<meta name="viewport" content="width=device-width,height=device-height, initial-scale=1, user-scalable=no">
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
	<link rel="stylesheet" href="https://bootswatch.com/4/slate/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="custom.css">
</head>


<body>
	  <div class="container" style="margin-top: 15%;">

		  		<div class="row h-100 justify-content-center align-items-center">
			    	<div class="card text-white bg-primary mb-3" style="width: 60%;">
					  <div class="card-header">
					  	<ul class="nav nav-tabs">
					  		<?php
						  	if (isset($_GET['error'])) {
						  		if ($_GET['error'] == "differentpwds") {
						  			echo '<li class="nav-item">
										    <a class="nav-link" data-toggle="tab" href="#login">Log In</a>
										  </li>
										  <li class="nav-item">
										    <a class="nav-link active" data-toggle="tab" href="#signup">Sign Up</a>
										  </li>';
						  		}
						  		else {
						  			echo '<li class="nav-item">
										    <a class="nav-link" data-toggle="tab" href="#login">Log In</a>
										  </li>
										  <li class="nav-item">
										    <a class="nav-link active" data-toggle="tab" href="#signup">Sign Up</a>
										  </li>';
						  		}
						  	}
						  	else {
						  		echo '<li class="nav-item">
									    <a class="nav-link active" data-toggle="tab" href="#login">Log In</a>
									  </li>
									  <li class="nav-item">
									    <a class="nav-link" data-toggle="tab" href="#signup">Sign Up</a>
									  </li>';
						  	}
						  	?>

						</ul>
					  </div>
					  <div class="card-body">
					    <div id="myTabContent" class="tab-content">
					    	<?php
						  	if (isset($_GET['error'])) {
						  		if ($_GET['error'] == "differentpwds") {
						  			echo '<div class="tab-pane fade" id="login">';
						  		}
						  		else {
						  			echo '<div class="tab-pane fade" id="login">';
						  		}
						  	}
						  	else {
						  		echo '<div class="tab-pane fade active show" id="login">';
						  	}
						  	?>
						    <div class="form">
						    	<form action="includes/login.php" method="post">
								  <fieldset>
								    <legend>Log In!!</legend>
								    <div class="form-group">
								      <label for="emailLogIn">Email</label>
								      <input type="email" class="form-control" name="email" aria-describedby="emailHelp" placeholder="Enter email" required>
								    </div>
								    <div class="form-group">
								      <label for="InputPassword1">Password</label>
								      <input type="password" class="form-control" name="password" placeholder="Password" required>
								    </div>
								    <div class="row h-100 justify-content-center align-items-center">
								    	<button type="submit" class="btn btn-primary" name='login'>Submit</button>
								    </div>
								  </fieldset>
								</form>
						    </div>
						  </div>
						  <?php
						  	if (isset($_GET['error'])) {
						  		if ($_GET['error'] == "differentpwds") {
						  			echo '<div class="tab-pane fade active show" id="signup">';
						  		}
						  		else {
						  			echo '<div class="tab-pane fade active show" id="signup">';
						  		}
						  	}
						  	else {
						  		echo '<div class="tab-pane fade" id="signup">';
						  	}
						  	?>
						  	<div class="form">
						    <form action="includes/signup.php" method="post">
							  <fieldset>
							    <legend>Sign Up!</legend>
							    <div class="form-group">
							      <label>First Name</label>
							      <input type="text" class="form-control" name="first_name" aria-describedby="emailHelp" placeholder="Enter Your First Name" required>
							    </div>
							    <div class="form-group">
							      <label>Last Name</label>
							      <input type="text" class="form-control" name="last_name" aria-describedby="emailHelp" placeholder="Enter Your Last Name" required>
							    </div>
							    <div class="form-group">
							      <label>Email address</label>
							      <input type="email" class="form-control" name="email_up" aria-describedby="emailHelp" placeholder="Enter Your Email" required>
							      <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
							    </div>
							    <div class="form-group">
								    <label>Gender</label>
								    <div class="form-check">

							        <label class="form-check-label">
							          <input type="radio" class="form-check-input" name="sex" id="optionsRadios1" value="M" checked>
							          Male
							        </label>
							      </div>
							      <div class="form-check">
							      <label class="form-check-label">
							          <input type="radio" class="form-check-input" name="sex" id="optionsRadios2" value="F">
							          Female
							        </label>
							      </div>
							     </div>
							     <div class="form-group">
							      <label>Age</label>
							      <input type="number" class="form-control" name="age" placeholder="Enter Your Age" required>
							    </div>
							    <?php
							  	if (isset($_GET['error'])) {
							  		if ($_GET['error'] == "differentpwds") {
							  			echo '<div class="form-group">
										      <label>Password</label>
										      <input type="password" name="pwd" class="form-control is-invalid" id="inputInvalid" required>
										      <div class="invalid-feedback">Sorry, different passwords. Try again</div>
										    </div>
										    <div class="form-group">
										      <label>Verify Password</label>
										      <input type="password" name="pwd2" class="form-control is-invalid" id="inputInvalid" required>
										      <div class="invalid-feedback">Sorry, different passwords. Try again</div>
										    </div>';
							  		}
							  		else {
							  			echo '<div class="form-group">
										      <label>Password</label>
										      <input type="password" class="form-control" name="pwd" placeholder="Enter a Password" required>
										    </div>
										    <div class="form-group">
										      <label>Verify Password</label>
										      <input type="password" class="form-control" name="pwd2" placeholder="Repeat Password" required>
										    </div>';
							  		}
							  	}
							  	else {
							  			echo '<div class="form-group">
										      <label>Password</label>
										      <input type="password" class="form-control" name="pwd" placeholder="Enter a Password" required>
										    </div>
										    <div class="form-group">
										      <label>Verify Password</label>
										      <input type="password" class="form-control" name="pwd2" placeholder="Repeat Password" required>
										    </div>';
							  		}
							  	?>

							    </fieldset>
							    <div class="row h-100 justify-content-center align-items-center">
							    	<button type="submit" class="btn btn-primary" name='register'>Submit</button>
							    </div>
							  </fieldset>
							</form>
						  </div>
						</div>
					  </div>
					</div>
				</div>

	</div>
</body>




</html>
