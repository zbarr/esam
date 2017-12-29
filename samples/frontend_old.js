var home = 'ws://192.168.1.69:8081'
var away = 'ws://192.168.70.56:8081'

var ws = new WebSocket(away)

var messageCount = 0

document.getElementById('header').innerHTML = "Scoreboard"

ws.onopen = function() {
    console.log('Websocket connected...')
    ws.send('connected')
}


var scoreboardProducts = ['LTC-BTC', 'ETH-BTC', 'BTC-USDT', 'LTC-USDT', 'BTC-USD', 'LTC-USD']


ws.onmessage = function (message) {

    var exchanges = JSON.parse(message.data)

    if (messageCount == 0) {
        //createTable(exchanges, 'LTC-BTC')
        createScoreboard(exchanges, scoreboardProducts)
    }

    //updateTable(exchanges, 'LTC-BTC')
    updateScoreboard(exchanges, scoreboardProducts)
    console.log(message)
    messageCount++
}

function updateTable(exchanges, product) {
    table = document.getElementById('content').childNodes[0]

    for (i = 0; i < exchanges.length; i++) {
        for (j = 0; j < exchanges.length; j++) {

            cell = table.rows[i+1].cells[j+1]
            ltp1 = exchanges[i].products[product].lastTradePrice
            ltp2 = exchanges[j].products[product].lastTradePrice

            if (i != j) {
                cell.textContent = ltp1 / ltp2
                if (Math.abs(1 - (ltp1/ltp2)) > .005) {
                    cell.style.backgroundColor = "green"
                }
                else {
                    cell.style.backgroundColor = null
                }
            }
            else {

                cell.textContent = ltp1

            }
        }
    }
}

function createTable(exchanges, product) {
    var row = null, table = document.createElement("table")
    table.className = "table table-hover table-bordered"

    row = table.insertRow()
    row.insertCell().textContent = product

    for (k = 0; k < exchanges.length; k++) {
        row.insertCell().textContent = exchanges[k].name
    }

    for (i = 0; i < exchanges.length; i++) {
        row = table.insertRow()
        row.insertCell().textContent = exchanges[i].name

        for (j = 0; j < exchanges.length; j++) {
            if (i != j) {
                row.insertCell().textContent = exchanges[i].products[product].lastTradePrice / exchanges[j].products[product].lastTradePrice
            }
            else {
                row.insertCell().textContent = exchanges[i].products[product].lastTradePrice
            }
        }
    }
    document.getElementById('content').appendChild(table)
}

function createScoreboard(exchanges, products) {
    var row = null, table = document.createElement("table")
    table.className = "table table-hover table-bordered"

    row = table.insertRow()
    row.insertCell().textContent = "Scoreboard"

    for (k = 0; k < products.length; k++) {
        row.insertCell().textContent = products[k]
    }

    for (i = 0; i < exchanges.length; i++) {
        row = table.insertRow()
        row.insertCell().textContent = exchanges[i].name

        for (j = 0; j < products.length; j++) {
            row.insertCell().textContent = null
        }
    }

    document.getElementById('content').appendChild(table)

}

function updateScoreboard(exchanges, products) {
    table = document.getElementById('content').childNodes[0]

    for (var i = 0; i < products.length; i++) {

        var quickArray = []

        for (var j = 0; j < exchanges.length; j++) {

            cell = table.rows[j+1].cells[i+1]

            if (exchanges[j].products[products[i]]) {
                if (exchanges[j].products[products[i]].lastTradePrice) {
                    cell.textContent = exchanges[j].products[products[i]].lastTradePrice
                    quickArray.push(cell)
                }
                else {
                    cell.textContent = "Waiting"
                }
            }
            else {
                cell.textContent = "Not Available"
            }

        }
        if (quickArray.length > 0) {
            colorizeCells(quickArray)
        }
    }
}

function colorizeCells(cellArray) {
    cellArray.sort(function(a, b) {
        return a.textContent - b.textContent
    })

    cellArray[0].style.backgroundColor = "red"

    for (var i = 1; i < (cellArray.length - 1); i ++) {
        cellArray[i].style.backgroundColor = "white"
    }

    cellArray[cellArray.length -1].style.backgroundColor = "green"

}

function updateClock () {
  var currentTime = new Date ( );

  var currentHours = currentTime.getHours ( );
  var currentMinutes = currentTime.getMinutes ( );
  var currentSeconds = currentTime.getSeconds ( );

  // Pad the minutes and seconds with leading zeros, if required
  currentMinutes = ( currentMinutes < 10 ? "0" : "" ) + currentMinutes;
  currentSeconds = ( currentSeconds < 10 ? "0" : "" ) + currentSeconds;

  // Choose either "AM" or "PM" as appropriate
  var timeOfDay = ( currentHours < 12 ) ? "AM" : "PM";

  // Convert the hours component to 12-hour format if needed
  //currentHours = ( currentHours > 12 ) ? currentHours - 12 : currentHours;

  // Convert an hours component of "0" to "12"
  //currentHours = ( currentHours == 0 ) ? 12 : currentHours;

  // Compose the string for display
  var currentTimeString = currentHours + ":" + currentMinutes + ":" + currentSeconds + " " + timeOfDay;

  // Update the time display
  document.getElementById("clock").innerHTML = currentTimeString;
}
