<!DOCTYPE html>
<html lang="en">
<head>
  <title>Vse konceptne kartice</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body>
<div class="container">
  <h2>Zbirka konceptnih kartic</h2>
  <p>Tukaj si lahko ogledate vse konceptne kartice v bazi.</p>            
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Naslov</th>
        <th>Ključne besede</th>
        <th>Orodje/jezik</th>
		<th>Ogled</th>
		<th>Uredi</th>
      </tr>
    </thead>
    <tbody>
	% for kartica in kartice:
       <tr>
		 <td>
	     {{kartica['naslov']}}
		 </td>
		 <td>
		 {{kljucne}}
		 </td>
		 <td>
	     {{kartica['orodja']}}
		 </td>
		 <td>
	     Ogled kartice
		 </td>
		 <td>
	     Uredi
		 </td>
	   </tr>
	% end
	
	 <div class="ui-widget">
         <label for="tags">Tag programming languages: </label>
         <input id="tags" size="50">
     </div>
	 
	 <div class="ui-widget">
         <label for="kljucne">Išči po ključnih besedah: </label>
         <input id="kljucne" size="50">
     </div>
	
    </tbody>
  </table>
</div>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <!--jQuery Autocomplete (https://jqueryui.com/autocomplete/#multiple)-->
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  <script>
  $( function() {
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion", 
      "Erlang",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme"
    ];
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
 
    $( "#tags" )
      // don't navigate away from the field on tab when selecting an item
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        minLength: 0,
        source: function( request, response ) {
          // delegate back to autocomplete, but extract the last term
          response( $.ui.autocomplete.filter(
            availableTags, extractLast( request.term ) ) );
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the comma-and-space at the end
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
      });
  } );
  </script>
  <script>
  $( function() {
    var myObj = { {{kljucne}} };
	var myJSON = JSON.stringify(myObj);
      return val.split( /,\s*/ );
    function split( val ) {
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
 
    $( "#kljucne" )
      // don't navigate away from the field on tab when selecting an item
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        minLength: 0,
        source: function( request, response ) {
          // delegate back to autocomplete, but extract the last term
          response( $.ui.autocomplete.filter(
            kljucneNaVoljo, extractLast( request.term ) ) );
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the comma-and-space at the end
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
      });
  } );
  </script>
  
</body>
</html>
