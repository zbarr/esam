var navbar_desks = document.getElementsByClassName("desk")
console.log(navbar_desks[0])
for (var i = 0; i < navbar_desks.length; i++) {
  navbar_desks[i].onclick = function() {
    resetActive()
    var desk = this.id.split("-")[1]
    getSapphires(desk)
  }
}

function getActiveHeartbeats() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", 'beats', true); // false for synchronous request
    xmlHttp.onload = function (err) {
        if (xmlHttp.readyState === 4) {
            if (xmlHttp.status === 200) {
                data = JSON.parse(xmlHttp.responseText)
                overlayBeats(data.pairs)
                //document.getElementById('page').innerHTML = JSON.stringify(data.pairs)
            } else {
                console.error(xmlHttp.statusText);
            }
        }
    }
    xmlHttp.onerror = function (e) {
      console.error(xmlHttp.statusText);
    };
    xmlHttp.send();
}


function organizedPanels(data) {
  var div0 = document.createElement("div")
  div0.className = "container-fluid"
  var count = 0
  for (desk in data) {
    if (((count + 1)/2) % 1 != 0) {
      var div1 = document.createElement("div")
      div1.className = "col-sm-12 col-md-6 col-lg-3 panel-group"
    }
    div0.appendChild(div1)
    div1.appendChild(createBasicPanel(desk, data[desk]))
    count++
  }

  return div0
}

function createBasicPanel(name, desk) {

  var div0 = document.createElement("div")
  div0.className = "panel"
  var div1 = document.createElement("div")
  div1.className = "panel-heading"
  //div1.innerHTML = name
  div0.appendChild(div1)
  var div3 = document.createElement("div")
  div3.className = "panel-title"
  div3.innerHTML = name
  div1.appendChild(div3)
  var div2 = document.createElement("div")
  div2.className = "panel-body"
  div0.appendChild(div2)
  var table = document.createElement("table")
  //div2.innerHTML = desk[i].name
  table.className = "table table-condensed"
  div2.appendChild(table)
  var body = document.createElement("tbody")
  table.appendChild(body)

  for (desk in data)
    for (i in desk) {

      var row = document.createElement("tr")
      row.id = desk[i].name
      body.appendChild(row)
      var td0 = document.createElement("td")
      td0.innerHTML = desk[i].suite + "-" + desk[i].name
      row.appendChild(td0)
      var td1 = document.createElement("td")
      td1.innerHTML = desk[i].host
      td1.setAttribute("align", "right")
      row.appendChild(td1)
    }
  return div0
}

function overlayBeats(beats) {
  for (i in beats) {
    try {
      document.getElementById(beats[i][1].split("-")[1]).className = "success"
    }
    catch(err) {
      console.log(beats[i][1].split("-")[1] + " is not available on this page.")
    }
  }
}
