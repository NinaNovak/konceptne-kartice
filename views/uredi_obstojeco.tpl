<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="ikone/{{favicon}}">

	<!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	<!-- Bootstrap JS -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
	
	<!-- jQuery -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="jquery.min.js"><\/script>')</script>
	
    <title>Posodobi kartico</title>

        <style><!-- v znački style je vsebina datotetke dashboard.css -->
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
  padding-top: 50px;
  
}
@media (min-width: 768px) {
  .main {
    padding-right: 40px;
    padding-left: 40px;
  }
}
.main .page-header {
  margin-top: 20px;
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

  

<form action="/uredi_obstojeco" method="post" enctype="multipart/form-data">
<div class="container-fluid">
  <h2>Posodabljanje kartice</h2>
  
  <h4>Naslov</h4>
  Obstoječi naslov kartice: <b><font color="CornflowerBlue ">{{kartice['naslov']}}</font></b><br>
  Novi naslov kartice: <input type="text" name="ime_kartice" size="50" />
  <input type="hidden" name="id_kartice" value={{id_kartice}}>
  </a>
  
  <h4>Datoteki</h4>
  
  <h5><i>Naloži PDF</i></h5>
  <input type="file" name="nalozi_docx" value="Naloži DOCX" />
  <h5><i>Naloži DOCX</i></h5>
  <input type="file" name="nalozi_pdf" value="Naloži PDF" />
  
  <h4>Jeziki / orodja</h4>
  <h5><i>Obstoječi</i></h5>
  Po potrebi odznačite jezike, ki jih ne želite več imeti:  <br>
    %for orod in orodj:
       <input type="checkbox" name="stara_orodja" checked value={{orod[0]}}>{{orod[1]}}<br>
    %end
  <h5><i>Novi</i></h5>
  Po potrebi dodajte nove jezike / orodja. Ločite jih z vejico: <br>
  Novi jeziki: 
  <input type="text" name="nova_orodja" size="50" /><!-- Kaj če 2 novi orodji? -->
  
  <h4>Ključne besede</h4>
  <h5><i>Obstoječe</i></h5>
  Po potrebi odznačite ključne besede, ki jih ne želite več imeti. <br>
  %for klj in kljucne:
       <input type="checkbox" name="nov_sez_kljucnih" checked value={{klj}} />{{klj}}<br>
  %end
  <h5><i>Nove</i></h5>
  Po potrebi dodajte nove ključne besede. Ločite jih z vejico: <br>
  Nove ključne besede: <input type="text" name="nove_kljucne" size="50" />
  </a><br>
  
  <h4>Kratek opis</h4>
  
  <h5><i>Obstoječi</i></h5>
  
  "{{opis}}"
  
  <h5><i>Novi</i></h5>
  <textarea name="opis" cols="50" rows="2"></textarea>
  <br><br>
  </a>
  
  <input type="submit" value="Oddaj popravke"  />
  <br><br><br>
</div>
  </form>
</div>

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