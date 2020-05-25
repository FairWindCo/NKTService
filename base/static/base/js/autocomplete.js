function createAutoCompleteMultiple(url,element, min_input_len=2){
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
     $(element).on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      }).autocomplete({
        source: function( request, response ) {
          $.getJSON( url, {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < min_input_len ) {
            return false;
          }
        },
        position: { my : "right top", at: "right center" },
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
}

function createAutoComplete(url,element, min_input_len=2, onselect){
    element=$(element).autocomplete({
        source: url,
        minLength: min_input_len
    });
    if(onselect){
        element.on( "autocompleteselect", onselect );
    }

}
