// Author - Zach Barr

console.log(window.location.host)
host = 'http://' + window.location.host

$(document).ready(function(){

  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on('connect', function() {
    console.log("connected!")
  });

  socket.on('test', function(msg) {
    console.log(msg.data)
  })

  socket.on('update', function(msg) {
    if (msg.data.type != "alert") {
      document.getElementById(msg.data.app_name).style.backgroundColor = msg.data.color
    }
    else {
      old_color = document.getElementById(msg.data.app_name).style.backgroundColor
      document.getElementById(msg.data.app_name).style.backgroundColor = msg.data.color
      setTimeout(function() {flash(msg.data.app_name, old_color);}, 500)
    }
  });

  socket.on('message', function(data) {
    console.log("received data")
  });

  socket.on('error', function(err) {
    console.log(err)
  });

  socket.on('reset', function() {
    $.get(window.location.href + "?view=true", function(data) {
      document.getElementById('page').innerHTML = data
    })
    console.log("Data refreshed.")
  })
});


var sidebar_desks = document.getElementsByClassName("sidebar-desk")
for (var i = 0; i < sidebar_desks.length; i++) {
  sidebar_desks[i].onclick = function() {
    resetActive()
    document.getElementById(this.id).classList.add("active")
    var desk = this.id.split("-").slice(1,).join("-")
    getDesks(desk)
  }
}

window.onpopstate = function(e){
    if(e.state){
      location.reload()
    }
};

/** Hamburger button **/
document.getElementById("sidebarCollapse").onclick = function(event) {
    $('#sidebar').toggleClass('active');
    console.log("toggling")
}

/** e7 Button **/
document.getElementById("e7").onclick = function (event) {
    resetActive()
    document.getElementById("home").classList.add("active")
    getHome()
}


/** Home Button **/
document.getElementById("home").onclick = function (event) {
    resetActive()
    document.getElementById("home").classList.add("active")
    getHome()
}

/** Suites Button **/
document.getElementById("suites").onclick = function (event) {
    resetActive()
    document.getElementById("suites").classList.add("active")
    getSuites()
}


/** Datacenters button **/
document.getElementById("datacenters").onclick = function (event) {
    resetActive()
    document.getElementById("datacenters").classList.add("active")
    getDatacenters()
}

/** Desks button **/
document.getElementById("desks").onclick = function (event) {
    resetActive()
    document.getElementById("desks").classList.add("active")
    getDesks()
}

/** Monitor button **/
document.getElementById("monitor").onclick = function (event) {
  resetActive()
  document.getElementById("monitor").classList.add("active")
  getMonitor()
}

/*******************************
Click Handlers for sidebar
*******************************/




function resetActive() {
    $('#navlinks li').removeClass('active');
    $('#sidebar-items .sidebar-desk').removeClass('active');
}

function getDatacenters() {
  $.get(host + "/datacenters?view=true", function(data) {
    document.getElementById('page').innerHTML = data
  })
  changeUrl("Datacenters",  host + "/datacenters")
}

function getHome() {
  $.get(host + "/home?view=true", function(data) {
    document.getElementById('page').innerHTML = data
  })
  changeUrl("Home",  host + "/")
}

function getSuites() {
  $.get(host + "/suites?view=true", function(data) {
    document.getElementById('page').innerHTML = data
  })
  changeUrl("Suites", host + "/suites")
}

function getMonitor() {
  $.get(host + "/monitor?view=true", function(data) {
    document.getElementById('page').innerHTML = data
  })
  changeUrl("Monitor", host + "/monitor")
}

function getDesks(desk = null) {
  query_string = "?view=true"
  if (desk) {
    page_title = "desks/" + desk
    page_url = host + "/desks/" + desk
  }
  else {
    page_title = "desks"
    page_url = host + "/desks"
  }
  $.get(page_url + query_string, function(data) {
    document.getElementById('page').innerHTML = data
  })
  changeUrl(page_title, page_url)
}

function changeUrl(title, url) {
    if (typeof (history.pushState) != "undefined") {
        var obj = { Title: title, Url: url };
        window.history.pushState(obj, obj.Title, obj.Url);
    } else {
        alert("Browser does not support HTML5.");
    }
}

function flash(app, color) {
  document.getElementById(app).style.backgroundColor = color
}
