$(document).ready(function() {
    var socketWorker = new Worker('js/socketWorker.js');
    var ctx = document.getElementById('chart-canvas').getContext('2d');
    var data = [];
    var maxTemp = 100;
    var minTemp = 30;

    var maxTempSet = -1;
    var minTempSet = -1;

    var doRender = true;
    var height = ctx.canvas.width;
    var width = ctx.canvas.height;
    var yRatio = height / (maxTemp - minTemp);

    var maxT = $('#max-temp'),
        minT = $('#min-temp');

    socketWorker.onmessage = function(e) {
        console.log(e.data);
        if (e.data['type'] === 'temp_hist') {
            data.push(e.data.temperature);
        } else if (e.data['type'] === 'max_temp') {
            maxTempSet = e.data.temperature
            maxT.val(maxTempSet);
            maxT.prop('disabled', false);
        } else if (e.data['type'] === 'min_temp') {
            minTempSet = e.data.temperature
            minT.val(minTempSet);
            minT.prop('disabled', false);
        }
        doRender = true;
    }

    var render = function() {
        ctx.lineWidth = 1;
        ctx.imageSmoothingEnabled = false;

        // fill background
        ctx.fillStyle = "#292929";
        ctx.fillRect(0,0,width,height);
        
        // temperature lines
        var numLines = parseInt((maxTemp - minTemp) / 10);
        var minTenth = parseInt(minTemp / 10) * 10;
        var j = 0;
        var lineColors = ["#888", "#666"];
        var textHeight = (height / numLines) / 2;
        textHeight = Math.min(textHeight, 16);
        textHeight = Math.max(textHeight, 10);
        ctx.font = '100 ' + textHeight + 'px sans-serif';
        for (var i = 0; i <= numLines + 1; i++) {
            var tempTenth = minTenth + (10 * i);
            var lineAt = (maxTemp - tempTenth) * yRatio;
            ctx.fillStyle = lineColors[j % 2];
            j++;
            ctx.fillRect(0, lineAt, width, 1);
            ctx.fillStyle = "#ccc";
            ctx.fillText(tempTenth + '°', 4, lineAt - 4);
        }
        
        var maxTempSetY = tempToY(maxTempSet),
            minTempSetY = tempToY(minTempSet);
        ctx.fillStyle = 'rgba(0,0,0,.2)';
        ctx.fillRect(0, maxTempSetY, width, minTempSetY - maxTempSetY)
        ctx.fillStyle = 'rgba(256,60,0,.8)';
        ctx.fillRect(0, maxTempSetY, width, 1);
        ctx.fillStyle = 'rgba(0,100,256,.8)';
        ctx.fillRect(0, minTempSetY, width, 1);

        if (data.length < 1) {
            return;
        }
        // cur temperature
        ctx.fillStyle = "#ccc";
        var curTemp = data[data.length-1];
        ctx.font = '100 30pt sans-serif';
        ctx.fillText(curTemp.toFixed(2) + '°', width - 120, height - 7);

        // data
        var len = data.length - 1;
        for (var i=len; i >= 0; i--) {
            var x = (len - i) * 3;
            x = width - x;
            ctx.moveTo(x,height);
            var y = (maxTemp - data[i]) * yRatio;
            ctx.fillStyle = 'rgba(256,256,256,.2)';
            ctx.fillRect(x, y, 1.5, height);
            if (y < tempToY(maxTempSet)) {
                ctx.fillStyle = '#F01E44';
            } else if (y > tempToY(minTempSet)) {
                ctx.fillStyle = 'dodgerBlue';
            } else {
                ctx.fillStyle = '#85E665';
            }
            ctx.fillRect(x - 1, y - 1, 2, 2);
        }
    }

    var tempToY = function(temp) {
        return (maxTemp - temp) * yRatio;
    }

    var lastDataLen = 0;
    var renderLoop = function() {
        if (doRender) {
            render();
        }
        lastDataLen = data.length;
        doRender = false;
        window.requestAnimationFrame(renderLoop);
    }

    var resize = function() {
        width = window.innerWidth;
        height = window.innerHeight;
        ctx.canvas.width = width;
        ctx.canvas.height = height;
        yRatio = height / (maxTemp - minTemp);
    }

    $(window).resize(resize);
    resize();
    renderLoop();

    window.onbeforeunload = function() {
        socketWorker.postMessage({
            type: 'close',
            data: null
        });
    }

    //menu
    $('#btn').click(function(e) {
        $('#btn').toggleClass('clicked');
        $('#menu').toggleClass('active');
    });

    maxT.val(maxTempSet);
    maxT.change(function(e) {
        maxT.prop('disabled', true);
        newVal = e.target.value;
        if (newVal < minTempSet) {
            newVal = minTempSet;
        }
        maxTempSet = newVal;
        doRender = true;
        socketWorker.postMessage({
            type: 'maxTempSet',
            data: parseInt(maxTempSet)
        });
    });

    minT.val(minTempSet);
    minT.change(function(e) {
        minT.prop('disabled', true);
        newVal = e.target.value;
        if (newVal > maxTempSet) {
            newVal = maxTempSet;
        }
        minTempSet = newVal
        doRender = true;
        socketWorker.postMessage({
            type: 'minTempSet',
            data: parseInt(minTempSet)
        });
    });
});
