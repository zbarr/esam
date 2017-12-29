const express = require('express')
var server = express()


//hooks up middleware
server.use(express.static(__dirname + '/public'));

var port = 8080
server.listen(port, function () {
    console.log((new Date()) + ' Server is listening on port ' + port)
})
