(function(){

    var get = function (path, depth=0) {
        if (depth > 3) {
          console.log('Too may \'get\'s. Returning.')
          return;
        }

        console.log(`GET to ${path}`);
        var xhttp = new XMLHttpRequest();
        xhttp.timeout = 5000; // 5 second timeout
        xhttp.ontimeout = function(e){
            alert('Request timed out for more than 5 seconds. Restarting');
            get('restart', depth+1);
        }

        xhttp.open('GET', path, true);
        xhttp.send();
    };

    var send_opcode = function (opcode){
        get('/signal/' + opcode);
    };

    var send_restart = function() {
      get('/restart');
    };

    // get all of our buttons that send signals
    var btns = document.getElementsByClassName('button');

    // register the callback on button click for each one
    for (var i = 0; i < btns.length; ++i){
        // register the XMLHttpRequest function to be called when we click
        // a button
        btns[i].addEventListener('click', function(event){
            var link = event.target.href;
            // add one to the index so we get just the opcode, not the slash
            // as well
            var last_slash_idx = link.lastIndexOf('/') + 1;
            var opcode = link.substr(last_slash_idx);
            event.preventDefault();
            send_opcode(opcode);
        });
    }

  var danger_btn = document.getElementById('restart');

  danger_btn.addEventListener('click', function(event){
      event.preventDefault();
      send_restart();
  });

})();
