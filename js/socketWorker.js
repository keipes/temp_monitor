var ws = new WebSocket("ws://localhost:8080/websocket");


ws.onmessage = function (evt) {
    var rcvd_data = JSON.parse(evt.data),
        date = new Date();
    // date.setTime(rcvd_data.timestamp);
    // chart.addData([rcvd_data.temperature], date.toTimeString());
    // if (chart.datasets[0].points.length > maxNodes) {
    //     chart.removeData();
    // }
    // _received_data.push(rcvd_data);
    console.log(rcvd_data);
    // postMessage(rcvd_data);
    postMessage(rcvd_data.temperature);
}.bind(this);

onmessage = function(e) {

}