<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

	<!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="jquery.min.js"><\/script>')</script>
    <script src="bootstrap.min.js"></script>
    <!-- Just to make our placeholder images work. Don't actually copy the next line! -->
    <script src="holder.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="ie10-viewport-bug-workaround.js"></script>	
	
    <title>Posodabljanje kartice {{kartice['naslov']}}</title>

    <!-- Bootstrap core CSS -->
    <link type="text/css" href="bootstrap.min.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link type="text/css" href="ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link type="text/css" href="dashboard.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>


    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
		  <!--kasneje naj spodnji href kaze na to (zacetno) stran-->
          <a class="navbar-brand" href="/dashboard">Zbirka konceptnih kartic</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
			<!--<li><a href="#">Jeziki</a></li>
            <li><a href="#">Ključne besede</a></li>-->
            <li><a href="/nalozi_novo_kartico">Dodaj kartico</a></li>
			<li><a href="/o_strani">O strani</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
		  % for orodje in orodja:
		    <li><a href="/dashboard?id_jezika={{orodje[0]}}">{{orodje[1]}}</a></li>
	      % end
          </ul>
        </div>
      <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">

  
  
<form action="/uredi_obstojeco" method="post" enctype="multipart/form-data">
  <h2>Posodabljanje kartice "<font color="CornflowerBlue "><i>{{kartice['naslov']}}</i></font>"</h2>
  
  <h4>Naslov</h4>
  Obstoječi naslov kartice: <b>{{kartice['naslov']}}</b><br>
  Novi naslov kartice: <input type="text" name="ime_kartice"  /> Predlagan slog poimenovanja kartice je <i>Ime jezika: Naslov kartice</i>.
  
  <h4>Datoteki</h4>
  
  <h5><i>Naloži PDF</i></h5>
  <input type="file" name="upload" value="Naloži DOCX" />
  <h5><i>Naloži DOCX</i></h5>
  <input type="file" name="upload" value="Naloži PDF" />
  
  <h4>Jeziki / orodja</h4>
  <h5><i>Obstoječi</i></h5>
  Po potrebi odznačite jezike, ki jih ne želite več imeti:  <br>
    %for orod in orodj:
       <input type="checkbox" name="orodje" checked value={{orod[0]}}>{{orod[1]}}<br>  
    %end
  <h5><i>Novi</i></h5>
  Po potrebi dodajte nove jezike / orodja. Ločite jih z vejico: <br>
  Novi jeziki: 
  <input type="text" name="jeziki" /><!-- Kaj če 2 novi orodji? -->
  
  <h4>Ključne besede</h4>
  <h5><i>Obstoječe</i></h5>
  Odznačite ključne besede, ki jih ne želite več imeti. <br>
  %for klj in kljucne:
       <input type="checkbox" name="klju" checked value={{klj}}>{{klj}}<br>
  %end
  <h5><i>Nove</i></h5>
  Naštejte nove ključne besede, ločene z vejicami. <br>
  Nove ključne besede: <input type="text" name="kljucne" />
  </a><br><br>
  
  <input type="submit" value="Oddaj popravke" disabled />
</form>

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
	<!-- Spodaj: za pop-over okence -->
	<script>
    $(document).ready(function(){
    $('[data-toggle="popover"]').popover();   
    });
    </script>



	</body>
</html>