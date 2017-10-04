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
	
    <title>Zbirka konceptnih kartic</title>

	<!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	
    <!-- Bootstrap core CSS -->
    <!--<link type="text/css" href="bootstrap.min.css" rel="stylesheet">-->

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link type="text/css" href="ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link type="text/css" href="/dashboard.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  <style>
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted black;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 120px;
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px 0;

    /* Position the tooltip */
    position: absolute;
    z-index: 1;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
}
</style>
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
          <a class="navbar-brand" href="dashboard">Zbirka konceptnih kartic</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
			<!--<li><a href="#">Jeziki</a></li>
            <li><a href="#">Ključne besede</a></li>-->
            <li><a href="/nalozi_novo_kartico">Dodaj kartico</a></li>
			<li><a href="/o_strani">O strani</a></li>
          </ul>
		    <form class="navbar-form navbar-right" action="" method="post">
              <input type="text" class="form-control" name="iskanje" placeholder="Išči...">
			  <button type="submit" class="btn btn-default">
			  <span class="glyphicon glyphicon-search"></span>
			  </button>
            </form>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
		  % for orodje in orodja:
		    <li><a href="dashboard?id_jezika={{orodje[0]}}">{{orodje[1]}}</a></li>
	      % end
          </ul>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">

		  <h2 class="sub-header" align="center">Orientacija</h2>
          <div class="row placeholders">
            <div class="col-xs-6 col-sm-3 placeholder">
              <img src="ikone/{{naj_kartica}}" width="100" height="100" class="img-responsive" alt="Slika">
              <h4>Glas ljudstva</h4>
			  <span class="text-muted">Največkrat ogledana kartica</span>
            </div>
            <div class="col-xs-6 col-sm-3 placeholder">
              <img src="ikone/{{kljucne}}" width="100" height="100" class="img-responsive" alt="Slika">
		      <span class="text-muted">Katere vsebine so v bazi?</span>
              <h4>Oblak ključnih besed</h4>
            </div>
            <div class="col-xs-6 col-sm-3 placeholder">
              <img src="ikone/{{naj_jezik}}" width="100" height="100" class="img-responsive" alt="Slika">
              <h4>Najbolj priljubljen jezik</h4>
			  <span class="text-muted">Največkrat iskani jezik ali orodje</span>
            </div>
            <div class="col-xs-6 col-sm-3 placeholder">
			  <a href="{{orodje[0]}}"><!--python vrne PDF random kartice-->
			  <img src="ikone/{{kliknasreco}}" width="100" height="100" class="img-responsive" alt="Slika">
              <h4>Klik na srečo</h4>
              <span class="text-muted">Izberi naključno kartico</span>
			  </a>
            </div>
          </div>

          <h2 class="sub-header" align="center">Vse kartice</h2>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
				  <th>Naslov</th>
                  <th>Jezik</th>
                  <th>Ključne besede</th>
                  <th>PDF</th>
				  <th>Izvorna<br>datoteka</th>
				  <th>Posodobi</th>
                </tr>
              </thead>
              <tbody>
					 % for kartica in kartice:
					 <tr>
					 
					 <td>
					   <a href="kartice/{{kartica['dat']}}">
					     <b>
					       <div title="{{kartica['opis']}}">
					         {{kartica['naslov']}}
					       </div>
					     </b>
					   </a>
					 </td>
					 
					 <td>
					   <i>{{kartica['orodja']}}</i>
					 </td>
					 
					 <td>
					   {{kartica['kljucne']}}
					 </td>
					 
					 <!--snemanje kartice PDF-->
					 <td style="text-align: center; vertical-align: middle;">
					   <a href="kartice/{{kartica['dat']}}">
   			             <div title="Prenesi PDF">
			               <span class="glyphicon glyphicon-download-alt"></span>
				           <!--alt="HTML tutorial" za Edge, če CSS dela, ikonce za DL in popravi pa ne-->
					     </div>
					   </a>
					 </td>
					 
					 <!--snemanje kartice DOCX, AI, TEX, ...-->
					 <td style="text-align: center; vertical-align: middle;">
					   <a href="kartice/{{kartica['dat']}}">
					     <div title="Prenesi datoteko za urejanje kartice">
					       <span class="glyphicon glyphicon-download-alt"></span>
					       <!--alt="HTML tutorial" za Edge, če CSS dela, ikonce za DL in popravi pa ne-->
					     </div>
					   </a>
					 </td>
					 
					 <!--spreminjanje obstojece kartice-->
					 <td style="text-align: center; vertical-align: middle;">
					   <a href="/uredi_obstojeco?id_kartice={{kartica[0]}}">
					      <div title="Posodobi kartico">
					        <span class="glyphicon glyphicon-cog"></span>
					      </div>
					   </a>
					 </td>
					 
					 </tr>
					 % end
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
   
  </body>
</html>
