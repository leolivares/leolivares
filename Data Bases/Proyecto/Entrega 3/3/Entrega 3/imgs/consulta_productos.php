<?php include 'includes/header.php'; ?>

<?php
if (!isset($_SESSION['user_id'])) {
header("Location: index.php");
exit();
}

?>

<h1>CONSULTA PRODUCTOS</h1>
