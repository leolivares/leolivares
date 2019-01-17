<?php
  try {
    $db_store = new PDO("pgsql:dbname=".DATABASE.";host=".HOST.";port=".PORT.";user=".USER.";password=".PASSWORD);
    $db_bank = new PDO("pgsql:dbname=".DATABASE2.";host=".HOST.";port=".PORT.";user=".USER2.";password=".PASSWORD2);
    }
    catch(PDOException $e) {
    echo $e->getMessage();
    }

    $fecha = date('Y-m-d');
    $id_user = $_SESSION['user_id'];

    if (isset($_GET['tpid'])) {
        $id_tienda = $_GET['tpid'];
        $in_cp = "INSERT INTO compraproducto VALUES (default, '$fecha', '$id_tienda', '$id_user');";
        $make_in_cp = $db_store -> prepare($in_cp);
        $make_in_cp -> execute();


        $get_last_id = "SELECT id_compra FROM compraproducto ORDER BY id_compra DESC LIMIT (1);";
        $last_id = $db_store -> prepare($get_last_id);
        $last_id -> execute();
        $last_compra = $last_id -> fetchAll();  
        $compra_id = $last_compra[0][0];

        $product_id = $_POST['product_id'];
        $cantidad = $_POST['qty'];
        $precio = $_POST['price'];

        $in_rcp = "INSERT INTO rcompraproducto VALUES ('$compra_id', '$product_id', '$cantidad');";
        $make_in_rcp = $db_store -> prepare($in_rcp);
        $make_in_rcp -> execute();

        $monto = $cantidad * $precio;
        $sql_pagos = "INSERT INTO pagos VALUES (default, '$id_user', '$id_tienda', '$monto', '$fecha');";
        $make_pago = $db_bank -> prepare($sql_pagos);
        $make_pago -> execute();


        $get_last_pid = "SELECT id_pago FROM pagos ORDER BY id_pago DESC LIMIT (1);";
        $last_pid = $db_bank -> prepare($get_last_pid);
        $last_pid -> execute();
        $last_pagoid = $last_pid -> fetchAll();  
        $pago_id = $last_pagoid[0][0];


        if ($_POST['dues'] != 0) {

            $count = 0;

            $por_cuota = $monto / $_POST['dues'];

            $date_now = date('Y-m-d');
            $pagado = 0;
            while ($count < $_POST['dues']) {
                
                // $time = strtotime($date_now);
                // $date_now = date("Y-m-d", strtotime("+1 month", $time));

                $sql_cuota = "INSERT INTO cuotas VALUES (default, '$pago_id', '$por_cuota', '$date_now', '$pagado');";
                $make_cuota = $db_bank -> prepare($sql_cuota);
                $make_cuota -> execute();

                $time = strtotime($date_now);
                $date_now = date("Y-m-d", strtotime("+1 month", $time));

                $count++;
            }

        }


    }
    else if (isset($_GET['tsid'])){
        $id_tienda = $_GET['tsid'];
        $fecha_exp = date('Y-m-d');
        $in_cs = "INSERT INTO compraservicio VALUES (default, '$id_tienda', '$id_user', '$fecha', '$fecha_exp');";
        $make_in_cs = $db_store -> prepare($in_cs);
        $make_in_cs -> execute();
 

        $get_last_id = "SELECT id_compraservicio FROM compraservicio ORDER BY id_compraservicio DESC LIMIT (1);";
        $last_id = $db_store -> prepare($get_last_id);
        $last_id -> execute();
        $last_servicio = $last_id -> fetchAll();  
        $compra_id = $last_servicio[0][0];

        $service_id = $_POST['servicio_id'];
        $precio = $_POST['price'];

        $in_rcs = "INSERT INTO rcompraservicio VALUES ('$service_id', '$compra_id');";
        $make_in_rcs = $db_store -> prepare($in_rcs);
        $make_in_rcs -> execute();

        $monto = $precio;
        $sql_pagos = "INSERT INTO pagos VALUES (default, '$id_user', '$id_tienda', '$monto', '$fecha');";
        $make_pago = $db_bank -> prepare($sql_pagos);
        $make_pago -> execute();


        $get_last_pid = "SELECT id_pago FROM pagos ORDER BY id_pago DESC LIMIT (1);";
        $last_pid = $db_bank -> prepare($get_last_pid);
        $last_pid -> execute();
        $last_pagoid = $last_pid -> fetchAll();  
        $pago_id = $last_pagoid[0][0];


        if ($_POST['dues'] != 0) {

            $count = 0;

            $por_cuota = $monto / $_POST['dues'];

            $date_now = date('Y-m-d');
            $pagado = 0;
            while ($count < $_POST['dues']) {
                
                // $time = strtotime($date_now);
                // $date_now = date("Y-m-d", strtotime("+1 month", $time));

                $sql_cuota = "INSERT INTO cuotas VALUES (default, '$pago_id', '$por_cuota', '$date_now', '$pagado');";
                $make_cuota = $db_bank -> prepare($sql_cuota);
                $make_cuota -> execute();

                $time = strtotime($date_now);
                $date_now = date("Y-m-d", strtotime("+1 month", $time));

                $count++;
            }

        }

    }


?>
