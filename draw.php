
<?php
//function for creating graph
function create() {
	//set variables from form
	$alue = $_POST["alue"];
	$uid = $_POST["uid"];
	$valinta1 = $_POST["valinta1"];
	$seperate = $_POST["seperate"];
	$operator = $_POST["operator"];
	$time = $_POST["time"];
	$long = "0";
	if(isset($seperate)){
		if(isset($operator)) {
			$seperate=$_POST["operator"];
		}
		else {
			$seperate="1";
		}
	}
	else {
		$seperate = "0";
	}
	if($time == "day"){
		$time = "0";
	}
	elseif($time == "week"){
		$time = "1";
	}
	else{
		$time = "0";
		$long = "1";
	}
	if(empty($alue)){
                $alue = "0";
        }
	if(empty($uid)) {
                $uid = "0";
        }
	else{
		$valinta1 = "0";
		$seperate = "0";
	}
	//create command for creating graph
        $cmnd = "python3 CreateGraph.py {$uid} {$alue} {$valinta1} {$long} {$time} 0 -150 1 {$seperate} 'testi.png'";

	//run command
	shell_exec($cmnd);
	}
?>


<!DOCTYPE html>
<html lang="fi">
<head>
  <title>Netradar-prototyyppi</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body style="background-color:#313538">
<nav class="navbar navbar-inverse" style="background-color:#313538">
  <img src="netradar.png" width="150" heigth="100" href="testi.html">
  <div class="container style="background-color:#313538"">
    <ul class="nav navbar-nav" style="color:#313538">
      <li><a href="esittely.html">Prototyypin esittely</a></li>
      <li><a href="parasoperaattori.html">Parhaan operaattorin valinta</a></li>
      <li><a href="piirra.html">Kuvaajien piirtotyökalut</a></li>
    </ul>
  </div>
</nav>
<div class="jumbotron text-center" style="background-color: #37b465">
  <h1>Kuinka hyvin mobiiliverkkosi toimii alueellasi?</h1>
  <!--<p>Prototyyppi on tuotettu osana Aalto-yliopiston Protopaja-kurssia</p>-->
  <div class="jumbotron text-center" style="background-color: #313538">
    <h1 style="color:white"></h1>
    <div class="container-fluid">
      <h1 style="color:#37b465">Tulokset: </h1>
       <?php
	create();
	echo "<img src='testi.png'  style='width:300;height:200;' class='img-responsive center-block'>";
       ?>
    </div>
  </div>
</div>
</body>
</html>
