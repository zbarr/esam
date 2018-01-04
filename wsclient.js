const zmq = require('zeromq');
var sock = zmq.socket('sub');

wsclient.run = function() {
    sock.connect("tcp://e7heartbeat:5589");
    sock.subscribe('')
    console.log('subscribe connected')

    sock.on('message', function(topic, message)  {
        console.log(topic.toString())
        sock.close()
    })
}
