(function(){

    var send_opcode = function (opcode){
        var xhttp = new XMLHttpRequest();
        xhttp.timeout = 5000; // 5 second timeout
        xhttp.ontimeout = function(e){
            alert("Request timed out for more than 5 seconds. Try again, and/or let Cameron know.");
        }
        xhttp.open("GET", "/signal/" + opcode, true);
        xhttp.send();
    }

    // get all of our buttons that send signals
    var btns = document.getElementsByClassName("button");

    // register the callback on button click for each one
    for (var i = 0; i < btns.length; ++i){
        // register the XMLHttpRequest function to be called when we click
        // a button
        btns[i].addEventListener('click', function(event){
            var link = event.target.href;
            // add one to the index so we get just the opcode, not the slash
            // as well
            var last_slash_idx = link.lastIndexOf("/") + 1;
            var opcode = link.substr(last_slash_idx);
            event.preventDefault();
            send_opcode(opcode);
        });
    }



})();
