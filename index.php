
<?php

//get postcodes from form
$postcodes = array($_POST["postinumero1"], $_POST["postinumero2"], $_POST["postinumero3"]);
//create command for Python function
$cmnd = "python3 /home/lehtinj14/protopaja/GetBestOperator.py {$postcodes[0]} {$postcodes[1]} {$postcodes[2]}";
$output = shell_exec($cmnd);
$length = strlen($output);
$startIndex = 0;
$endIndex = 0;
$myarray = array();
//parse python function's output
for($i=0; $i<$length; $i++){
        if($output[$i] == "[" && $output[$i+1] =="[" ){
                $startIndex = $i + 2;
        }
        elseif($startIndex > 0 && $output[$i] == "]" && $endIndex + 1 != $i){
                $endIndex = $i;
                $tulos = substr($output, $startIndex, $endIndex - $startIndex);
                array_push($myarray, array(explode(",",$tulos)));
        }
        elseif($startIndex > 0 && $output[$i] == "["){
                $startIndex = $i + 1;
        }
}
//get right values from freshly created array
$firstoperator = str_replace("'", "", $myarray[0][0][0]);
$secondoperator = str_replace("'", "", $myarray[1][0][0]);
$thirdoperator = str_replace("'", "", $myarray[2][0][0]);
$postalcode = str_replace("'", "", $myarray[0][0][1]);
$postalcode2 = str_replace("'", "", $myarray[0][0][4]);
$postalcode3 = str_replace("'", "", $myarray[0][0][7]);
$firstoppoints = $myarray[0][0][2];
$firstoppoints2 = $myarray[0][0][5];
$firstoppoints3 = $myarray[0][0][8];
$secondoppoints = $myarray[1][0][2];
$secondoppoints2 = $myarray[1][0][5];
$secondoppoints3 = $myarray[1][0][8];
$thirdoppoints = $myarray[2][0][2];
$thirdoppoints2 = $myarray[2][0][5];
$thirdoppoints3 = $myarray[2][0][8];
$firstopconfidence = $myarray[0][0][3];
$firstopconfidence2 = $myarray[0][0][6];
$firstopconfidence3 = $myarray[0][0][9];
$secondopconfidence = $myarray[1][0][3];
$secondopconfidence2 = $myarray[1][0][6];
$secondopconfidence3 = $myarray[1][0][9];
$thirdopconfidence = $myarray[2][0][3];
$thirdopconfidence2 = $myarray[2][0][6];
$thirdopconfidence3 = $myarray[2][0][9];
$firstopaverage = end($myarray[0][0]);
$secondopaverage = end($myarray[1][0]);
$thirdopaverage = end($myarray[2][0]);

$amountOfCodes = 1;
if(max(array(count($myarray[0][0]), count($myarray[1][0]), count($myarray[2][0]))) == 8){
	echo "moika";
	$amountOfCodes = 2;
}
elseif(max(array(count($myarray[0][0]), count($myarray[1][0]), count($myarray[2][0]))) > 8){
	$amountOfCodes = 3;
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
  <h1>Mikä operaattori toimii parhaiten alueellani?</h1>
  <!--<p>Prototyyppi on tuotettu osana Aalto-yliopiston Protopaja-kurssia</p>-->
  <div class="jumbotron text-center" style="background-color: #313538">
    <h1 style="color:white"></h1>
    <div class="container-fluid">
      <h1 style="color:#37b465">Tulokset: </h1>
       <?php
         if($amountOfCodes == 1){
        echo "<div class='row'>
	<div class='col-sm-4' style='background-color:#37b465'>
          <h3>{$firstoperator}</h3>
          <h4>{$postalcode}</h4>
          <h4>Saamat pisteet: {$firstoppoints}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$firstopconfidence}/5</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h3>{$secondoperator}</h3>
          <h4>{$postalcode}</h4>
          <h4>Saamat pisteet: {$secondoppoints}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$secondopconfidence}/5</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h3>{$thirdoperator}</h3>
          <h4>{$postalcode}</h4>
          <h4>Saamat pisteet: {$thirdoppoints}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$thirdopconfidence}/5</h4>
        </div>
      </div>";
      }
      elseif($amountOfCodes == 2) {
        echo "<div class='row'>
	<div class='col-sm-4' style='background-color:#37b465'>
          <h3>{$firstoperator}</h3>
          <h4>{$postalcode}</h4>
          <h4>Saamat pisteet: {$firstoppoints}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$firstopconfidence}/5</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h3>{$secondoperator}</h3>
          <h4>{$postalcode}</h4>
          <h4>Saamat pisteet: {$secondoppoints}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$secondopconfidence}/5</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h3>{$thirdoperator}</h3>
          <h4>{$postalcode}</h4>
          <h4>Saamat pisteet: {$thirdoppoints}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$thirdopconfidence}/5</h4>
        </div>
      </div>
      <div class='row'>
	<div class='col-sm-4' style='background-color:#37b465'>
          <h4>{$postalcode2}</h4>
          <h4>Saamat pisteet: {$firstoppoints2}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$firstopconfidence2}/5</h4>
          <br></br>
          <h4>Pisteiden keskiarvo: {$firstopaverage}</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h4>{$postalcode2}</h4>
          <h4>Saamat pisteet: {$secondoppoints2}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$secondopconfidence2}/5</h4>
          <br></br>
          <h4>Pisteiden keskiarvo: {$secondopaverage}</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h4>{$postalcode2}</h4>
          <h4>Saamat pisteet: {$thirdoppoints2}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$thirdopconfidence2}/5</h4>
          <br></br>
          <h4>Pisteiden keskiarvo: {$thirdopaverage}</h4>
        </div>
      </div>";
        }
	else {
	echo "<div class='row'>
	<div class='col-sm-4' style='background-color:#37b465'>
          <h3>{$firstoperator}</h3>
          <h4>{$postalcode}</h4>
          <h4>Saamat pisteet: {$firstoppoints}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$firstopconfidence}/5</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h3>{$secondoperator}</h3>
          <h4>{$postalcode}</h4>
          <h4>Saamat pisteet: {$secondoppoints}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$secondopconfidence}/5</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h3>{$thirdoperator}</h3>
          <h4>{$postalcode}</h4>
          <h4>Saamat pisteet: {$thirdoppoints}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$thirdopconfidence}/5</h4>
        </div>
      </div>
      <div class='row'>
	<div class='col-sm-4' style='background-color:#37b465'>
          <h4>{$postalcode2}</h4>
          <h4>Saamat pisteet: {$firstoppoints2}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$firstopconfidence2}/5</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h4>{$postalcode2}</h4>
          <h4>Saamat pisteet: {$secondoppoints2}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$secondopconfidence2}/5</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h4>{$postalcode2}</h4>
          <h4>Saamat pisteet: {$thirdoppoints2}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$thirdopconfidence2}/5</h4>
        </div>
      </div>
      <div class='row'>
	<div class='col-sm-4' style='background-color:#37b465'>
          <h4>{$postalcode3}</h4>
          <h4>Saamat pisteet: {$firstoppoints3}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$firstopconfidence3}/5</h4>
	  <br></br>
          <h4>Pisteiden keskiarvo: {$firstopaverage}</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h4>{$postalcode3}</h4>
          <h4>Saamat pisteet: {$secondoppoints3}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$secondopconfidence3}/5</h4>
	  <br></br>
          <h4>Pisteiden keskiarvo: {$secondopaverage}</h4>
        </div>
        <div class='col-sm-4' style='background-color:#37b465'>
          <h4>{$postalcode3}</h4>
          <h4>Saamat pisteet: {$thirdoppoints3}/8</h4>
          <h4>Arvio pisteiden luotettavuudelle: {$thirdopconfidence3}/5</h4>
	  <br></br>
          <h4>Pisteiden keskiarvo: {$thirdopaverage}</h4>
        </div>
      </div>";
	}?>
    </div>
  </div>
</div>
</body>
</html>
