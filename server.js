const express = require('express')
const childProcess = require('child_process');
const zmq = require('zeromq');
const path = require('path')


var app = express()
var router = express.Router();



var spawn = require('child_process').spawn
var py = spawn('bash', ['dbcreator.sh'])
var data = ""
var datastring = ""
var alldata = {}
alldata.pairs = []


py.stdout.on('data', function(data){
    datastring += data.toString();
    alldata.pairs.push(datastring.split(" "))
});

console.log(alldata)

var beats = ""

app.use(router)
app.use(express.static(path.join(__dirname, 'public')));


router.get('/', function(req, res) {
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

        beats = JSON.stringify(response)
        console.log("saved the beats")

    })

    res.sendFile(path.join(__dirname, '/public/index.html'))
})

router.get('/beats', function(req, res) {
    console.log("sending beats")
    res.send(beats)
})




var port = 8080
app.listen(port, function () {
    console.log((new Date()) + ' Server is listening on port ' + port)
})
