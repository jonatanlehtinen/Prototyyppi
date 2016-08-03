<?php
$postcodes = array($_POST["postinumero1"], $_POST["postinumero2"], $_POST["postinumero3"]);
$cmnd = "python3 GetBestOperator.py {$postcodes[0]} {$postcodes[1]} {$postcodes[2]}";
$output = shell_exec($cmnd);
$length = strlen($output);
$startIndex = 0;
$endIndex = 0;
$myarray = array();
//$result = json_decode($output, true);
//var_dump($result);
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
//var_dump($myarray);
//$cmnd = "python3 -c 'import GetBestOperator; GetOperator.getTheBestOperator([{$postcodes[0]}])'";
//$output =  shell_exec($cmnd);
//$output = exec("GetTheBestOperator.py 02150");
//var_dump($output);
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
      <li><a href="parasoperaattori.html">Parhaan operaattorin valinta</a></li>
      <li><a href="esittely.html">Prototyypin esittely</a></li>
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
      <div class="row">
        <div class="col-sm-4" style="background-color:#37b465"><?php echo str_replace("'", "", $myarray[0][0][0]);?></div>
        <div class="col-sm-4" style="background-color:#37b465"><?php echo str_replace("'", "", $myarray[1][0][0]);?></div>
        <div class="col-sm-4" style="background-color:#37b465"><?php echo str_replace("'", "", $myarray[2][0][0]);?></div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
<?php
var_dump($myarray);
?>
