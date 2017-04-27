<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Dodajanje nove kartice</title>
    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
	
<div class="container">
  <h3>Vnesite novo konceptno kartico</h3>

<!--   <form action="/upload" method="post" enctype="multipart/form-data">
  Category:      <input type="text" name="category" />
  Select a file: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
  </form>
  <br>
  <br> -->
  
  <form>
	<input type="file" class="filestyle" name="nalozena_dat" id="nalozena_dat" data-buttonBefore="true">
    <div class="form-group">
      <label for="naslov_kartice">Vnesite naslov kartice:</label>
      <input type="text" class="form-control" id="naslov_kartice" placeholder="Vnesite naslov kartice">
    </div>
	
    <div class="form-group">
      <label for="kljucne">Vnesite ključne besede, po katerih lahko kartico poiščemo v bazi:</label>
      <input type="text" class="form-control" id="kljucne" placeholder="Vnesite ključne besede">
    </div>
	
	Označite programski jezik, ki ga kartica uči (lahko označite več izbir): 
<label class="checkbox-inline"><input type="checkbox" value="python">Python</label>
<label class="checkbox-inline"><input type="checkbox" value="csharp">C#</label>
<label class="checkbox-inline"><input type="checkbox" value="scratch">Scratch</label>
<label class="checkbox-inline"><input type="checkbox" value="appinventor">App Inventor</label><br>



    <button type="submit" class="btn btn-default">Shranite kartico v bazo</button>
	
  </form>
</div>	

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>