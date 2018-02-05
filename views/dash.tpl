<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="ikone/{{ico_ikona}}">

	<!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	<!-- Bootstrap JS -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
	
	<!-- jQuery -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="jquery.min.js"><\/script>')</script>
	
    <title>Zbirka konceptnih kartic</title>

    <style><!-- v znački style je dashboard.css -->
/*
 * Base structure
 */

/* Move down content because we have a fixed navbar that is 50px tall */
body {
  padding-top: 50px;
}


/*
 * Global add-ons
 */

.sub-header {
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

/*
 * Top navigation
 * Hide default border to remove 1px line.
 */
.navbar-fixed-top {
  border: 0;
}

/*
 * Sidebar
 */

/* Hide for mobile, show later */
.sidebar {
  display: none;
}
@media (min-width: 768px) {
  .sidebar {
    position: fixed;
    top: 51px;
    bottom: 0;
    left: 0;
    z-index: 1000;
    display: block;
    padding: 20px;
    overflow-x: hidden;
    overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
    background-color: #f5f5f5;
    border-right: 1px solid #eee;
  }
}

/* Sidebar navigation */
.nav-sidebar {
  margin-right: -21px; /* 20px padding + 1px border */
  margin-bottom: 20px;
  margin-left: -20px;
}
.nav-sidebar > li > a {
  padding-right: 20px;
  padding-left: 20px;
}
.nav-sidebar > .active > a,
.nav-sidebar > .active > a:hover,
.nav-sidebar > .active > a:focus {
  color: #fff;
  background-color: #428bca;
}


/*
 * Main content
 */

.main {
  padding: 20px;
}
@media (min-width: 768px) {
  .main {
    padding-right: 40px;
    padding-left: 40px;
  }
}
.main .page-header {
  margin-top: 0;
}


/*
 * Placeholder dashboard ideas
 */

.placeholders {
  margin-bottom: 30px;
  text-align: center;
}
.placeholders h4 {
  margin-bottom: 0;
}
.placeholder {
  margin-bottom: 20px;
}
.placeholder img {
  display: inline-block;
  border-radius: 50%;
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
			<li><a href="/igrisce">Igrišče</a></li>
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
		  <h1 class="page-header">Novi obiskovalci lahko začnejo tukaj</h1>
          <div class="row placeholders">
		  
            <div class="col-xs-6 col-sm-3 placeholder">
			  <a href="kartice/{{nakljucna}}"><!--nakljucna-python izbere ime PDF datoteke nakljucne kartice-->
			    <img src="ikone/{{kliknasreco}}" width="100" height="100" class="img-responsive" alt="Slika4">
                 <h4>Klik na srečo</h4>
                <span class="text-muted">Naključna kartica</span>
			  </a>
			</div>
            <div class="col-xs-6 col-sm-3 placeholder">
			  <a href="tiralica">
              <img src="ikone/{{naj_jezik}}" width="100" height="100" class="img-responsive" alt="Slika3">
              <h4>Tiralica</h4>
			  <span class="text-muted">Največkrat iskano geslo</span>
			  </a>
            </div>
            <div class="col-xs-6 col-sm-3 placeholder">
			  <a href="kartice/{{max_ogledov}}">
                <img src="ikone/{{naj_kartica}}" width="100" height="100" class="img-responsive" alt="Slika1">
                <h4>Glas ljudstva</h4>
			    <span class="text-muted">Največkrat ogledana kartica</span>
              </a>
			</div>
            <div class="col-xs-6 col-sm-3 placeholder">
			  <a href="oblak">
              <img src="ikone/{{kljucne}}" width="100" height="100" class="img-responsive" alt="Slika2">
			  <h4>Oblak ključnih besed</h4>
		      <span class="text-muted">Katere vsebine so v bazi?</span>
			  </a>
            </div>			

          </div>

          <h1 class="page-header">Baza kartic{{katere}}</h1>
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
					   <a href="kartice/{{kartica['dat_orig']}}">
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
