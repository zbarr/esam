const express = require('express')
const childProcess = require('child_process');
const zmq = require('zeromq');
const path = require('path')

var app = express()
var router = express.Router();


const exec = require('child_process').exec, child
var sh = exec('bash dbcreator.sh')
var engines = []
var count = 0
var desks = {}

console.log("Parsing YAMLs...")
sh.stdout.on('data', function(data){
    enginearray = data.split("\n")
    for (var i = 0; i < enginearray.length; i++) {
        if (enginearray[i].includes('version')) {
            var engine = JSON.parse(enginearray[i])
            engines.push(engine)
            if (!(desks[engine['desk']])) {
                desks[engine['desk']] = []
            }

            desks[engine['desk']].push({
                'name': engine['name'],
                'version': engine['version'],
                'host': engine['host']
            })

        }
    }
    //console.log(desks)
});

sh.stderr.on('data', function(data) {
    console.log(data)
})

sh.stdout.on('close', function(){
    console.log("YAML Parsing Complete.")
})



var beats = ""

app.set('view engine', 'pug')
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

    //res.sendFile(path.join(__dirname, '/public/index.html'))
    res.render('index', desks)


    res.render('index')
})

router.get('/beats', function(req, res) {
    console.log("sending beats")
    res.send(beats)
})




var port = 8080
app.listen(port, function () {
    console.log((new Date()) + ' Server is listening on port ' + port)
})
