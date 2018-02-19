var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

var socket = new WebSocket(ws_scheme + '://' + window.location.host + '/dashboard/search');

socket.onopen = function open() {
    console.log('WebSockets connection created.');
};

socket.onmessage = function(event){
    processTweets(event);
};

if (socket.readyState == WebSocket.OPEN) {
    socket.onopen();
}

function pageReload() {
    location.reload();
}