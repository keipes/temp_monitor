$(document).ready(function() {
    var socketWorker = new Worker('js/socketWorker.js');
    var ctx = document.getElementById('chart-canvas').getContext('2d');
    console.log(ctx);

    var data = [];
    var maxTemp = 100;
    var minTemp = 32;

    socketWorker.onmessage = function(e) {
        data.push(e.data);
    }

    var render = function() {
        ctx.lineWidth = 1;
        ctx.imageSmoothingEnabled = false;
        var width = ctx.canvas.width,
            height = ctx.canvas.height;
        ctx.fillStyle = "#292929";
        ctx.fillRect(0,0,width,height);
        ctx.fillStyle = 'dodgerBlue';
        var len = data.length - 1;
        var yRatio = height / (maxTemp - minTemp);
        for (var i=len; i >= 0; i--) {
            var x = (len - i) * 2;
            x = width - x;
            ctx.moveTo(x,height);
            var y = (maxTemp - data[i]) * yRatio;
            ctx.fillRect(x, y, 1, height);
        }
        window.requestAnimationFrame(render);
    }

    var lastDataLen = 0;
    var renderLoop = function() {
        if (data.length !== lastDataLen) {
            render();
        }
        lastDataLen = data.length;
        window.requestAnimationFrame(renderLoop);
    }
    renderLoop();


    // var make_data = function() {
    //     var dates = [];
    //     var temperatures = [];
    //     var date = new Date();
    //     _received_data.forEach(function(el, idx) {
    //         var date = new Date();
    //         date.setTime(el.timestamp);
    //         var ts = date.toTimeString();
    //         dates.push(ts);
    //         temperatures.push(el.temperature);
    //     });
    //     return [dates, temperatures];
    // }.bind(this);

});
