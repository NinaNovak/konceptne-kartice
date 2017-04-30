<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Urejanje konceptne kartice</title>
    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>

<form action="/nalozi_novo_kartico" method="post" enctype="multipart/form-data">
  <h3>Nalaganje nove kartice</h3>
  Ime kartice: <input type="text" name="ime_kartice" /><br><br>
  <input type="file" name="upload" value="Naloži datoteko" />
  <h3>Orodje / programski jezik, ki ga uči kartica</h3>
  Najprej so našteta imena orodij, ki se začnejo z veliko začetnico,
  nato pa še imena, ki se začnejo z malo začetnico.<br><br>
  Možno je obkljukati več orodij. Če orodja ni med naštetimi, izpolniti polje 'Drugo'.<br><br><!-- Kaj če 2 novi orodji? -->
    %for orod in orodja:
       <input type="checkbox" name="orodje" value={{orod[0]}}>{{orod[1]}}
    %end
	   <!-- Dodatni checkbox za novo orodje -->
	   <input type="checkbox" class="oznaci">Drugo:<input type="text" name="novo" class="novo_orodje" /><br>
	   
  <h3>Ključne besede, po katerih se kartica lahko najde</h3><input type="text" name="kljucne" placeholder="Ključne besede ločite z vejico" /><br><br>
  <input type="submit" value="Vnesi kartico v bazo" />
</form>a


    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
	<script src="js/check_novo_orodje.js"></script>
	<!-- Spodaj: check_novo_orodje.js, ker samo z zgornjim src-jem ne deluje ... -->
	<script type="text/javascript">
    	$(".novo_orodje").on("keyup", function(e){
            if(this.value!=""){
                $(".oznaci").prop("checked", "checked");
            }else{
                $(".oznaci").prop("checked", ""); 
            }
        });
    </script>
  </body>
</html>