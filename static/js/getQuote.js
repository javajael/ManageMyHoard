"use strict";


// PART 1: SHOW A FORTUNE

// Written now to use an inline function for the event handler,
// and to use the $.load() method
$(function() {
  // all of your code goes inside here

    $('#get-quote-button').on('click', function (evt) {
        /*$("#quote-text").load('/get_quote');*/
        $.get('/get_quote', function (results) {
            $("#quote-text").html(results);
        });
    });
});