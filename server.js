const express = require('express')
var server = express()

const childProcess = require('child_process');

const zmq = require('zeromq');


server.get('/beats', function (req, res) {

    var data = []
    var response = {}
    response.pairs = []
    var sock = zmq.socket('sub');
    sock.connect("tcp://e7heartbeat:5589");
    sock.subscribe('')
    console.log('Subscribed to heartbeat snapshot.')

    sock.on('message', function(topic, message)  {
        sock.close()
        console.log("Connection closed to heartbeat snapshot.")
        data = topic.toString().split('\n')

        for (var i = 0; i < data.length - 1; i++) {
            dataarray = data[i].replace(" ", "").split('\t')
            if (dataarray.length == 2) {
                response.pairs.push(dataarray)
            }
            else {
                console.log("Discarded data: " + dataarray)
            }
        }

        res.send(JSON.stringify(response))
        console.log("Response to /beats sent.")
    })

    res.setHeader('Content-Type', 'application/json');
})


server.use(express.static('public'), function (req, res) {
    console.log(req)
});







var port = 8080
server.listen(port, function () {
    console.log((new Date()) + ' Server is listening on port ' + port)
})
