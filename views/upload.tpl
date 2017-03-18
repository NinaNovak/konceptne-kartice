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

<form action="/nalozi_novo_kartico" method="post" enctype="multipart/form-data">
  <h3>Nalaganje nove kartice</h3>
  Ime kartice: <input type="text" name="ime_kartice" /><br><br>
  <input type="file" name="upload" value="Naloži datoteko" />
  <h3>Orodje / programski jezik, ki ga uči kartica (možno je obkljukati več možnosti)</h3>
  <input type="checkbox" name="orodje" value="Python">Python<br>
  <input type="checkbox" name="orodje" value="C#">C#<br><br>
  Ključne besede, po katerih se kartica lahko najde<input type="text" name="kljucne" placeholder="Ključne besede ločite z vejico" /><br><br>
  <input type="submit" value="Vnesi kartico v bazo" />
</form>


    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>