var initWebSocket = function() {
    console.log('init web socket');
    var ws = new WebSocket("ws://localhost:8080/websocket");

    ws.onopen = function() {
        console.log('open');
        ws.send(JSON.stringify({
            type: 'hello',
            data: ''
        }));
    }
    ws.onmessage = function(evt) {
        var rcvd_data = JSON.parse(evt.data);
        postMessage(rcvd_data);
    };
    ws.onclose = function() {
        console.log('closing in ws.onclose');
        setTimeout(function() {
          initWebSocket();
        }, 1000);
    }
    onmessage = function(e) {
        if (e.data.type === 'close') {
            console.log('closing');
            ws.onclose = function() {};
            ws.close();
        } else {
            ws.send(JSON.stringify(e.data));
        }
    };

}
initWebSocket();
