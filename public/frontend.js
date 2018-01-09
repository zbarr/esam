//wsclient.run()



var errors = ['ch6pslt068.concord.global:: 2018-01-03,05:30:20.381303999 [ERROR] controller(54308) ccs2/PositionProxy.cpp:604 | INVALID POD SNAP: DPSIEE: 2|6|6|5000222560|26|2: [GrossPosition(100|200000000),IntradayPosition(100|200000000)]: strategy 6 no longer belongs to portfolio 6',
'ch6pslt068.concord.global:: 2018-01-03,05:30:20.381249644 [ERROR] controller(54308) ccs2/PositionProxy.cpp:604 | INVALID POD SNAP: DPSIEE: 2|39|145|5000091372|2|25: [GrossPosition(104|0),IntradayPosition(0|0)]: strategy 145 no longer belongs to portfolio 39',
'ch6psltr099.concord.global:: 2018-01-03,05:17:33.277005003 [ERROR] treasuries(7110) treas_strat/Scalper.h:93 | ZCN8 Emergency Wide 3',
'ch6psltr070.concord.global:: 2018-01-03,04:55:45.106732612 [ERROR] treasuries(9206) treas_strat/Scalper.h:93 | ZFH8 Emergency Wide 3',
'ch6psltr055.concord.global:: 2018-01-03,03:57:04.948013801 [ERROR] treasuries(67413) treas_strat/Scalper.h:95 | Emergency Wide 2']


var desks = {equities: {engines: ['es_stacker_01', 'equities_01', 'equities_02', 'equities_03', 'equities_04', 'equities_05', 'equities_06', 'equities_07']},
            cpcv: {engines: ['vmm_01', 'vmm_02', 'vmm_03']},
            bgls: {engines: ['bgls_01', 'bgls_02', 'bgls_03']},
            gas: {engines: ['gas_01', 'gas_02', 'gas_03']},
            treasuries: {engines: ['treasuries_01', 'treasuries_02']},
            ssvcs: {engines: ['pricefeeder-basic_glbx_01', 'pricefeeder-basic_zbbf_01', 'drop-ccs2-lime-1', 'ccs2-webadmin']}}


var sapphires = []

for (desk in desks) {
    sapphires = sapphires.concat(desks[desk].engines)
}


if (document.getElementById("sapphires").classList.contains("active")) {
    for (var i = 0; i < sapphires.length; i++) {
        div1 = document.createElement("div");
        div1.className="col-md-4";
        document.getElementById("grid").appendChild(div1);
        div2 = document.createElement("div");
        div2.className="panel";
        div1.appendChild(div2);
        div3 = document.createElement("div");
        div3.className="panel-heading";
        div2.appendChild(div3);
        div4 = document.createElement("div");
        div4.className="panel-body";
        div4.innerHTML = sapphires[i]
        div3.appendChild(div4);
    }
    console.log("here")
}


/** Hamburger button **/
document.getElementById("sidebarCollapse").onclick = function(event) {
    $('#sidebar').toggleClass('active');
    console.log("toggling")
}


/** Home Button **/
document.getElementById("home").onclick = function (event) {
    resetActive()
    document.getElementById("home").classList.add("active")
    getActiveHeartbeats()
}


/** Sapphires Button **/
document.getElementById("sapphires").onclick = function(event) {
    resetActive()
    document.getElementById("sapphires").classList.add("active")
    getSapphires()
    /**
    document.getElementById("page").innerHTML = ""

    for (var i = 0; i < sapphires.length; i++) {

        var div = document.createElement("div");
        div.className = "row"
        div.id="grid"
        document.getElementById("page").appendChild(div)
        var div1 = document.createElement("div");
        div1.className="col-md-3";
        document.getElementById("grid").appendChild(div1)
        var div2 = document.createElement("div");
        div2.className="panel panel-success";
        div1.appendChild(div2);
        var div3 = document.createElement("div");
        div3.className="panel-heading";

        // Header
        div3.innerHTML = sapphires[i] + " - ch6psltr079"
        // End header

        div2.appendChild(div3);

        var div4 = document.createElement("div");
        div4.className="panel-body";
        div2.appendChild(div4);

        var div = document.createElement("div");
        div.className="container-fluid"
        div4.appendChild(div)

        var btn = document.createElement("button");
        btn.className = "btn btn-success";
        btn.type="button"
        btn.innerHTML = "Start"
        div.appendChild(btn)

        var btn = document.createElement("button");
        btn.className = "btn btn-danger";
        btn.type="button"
        btn.innerHTML = "Stop"
        div.appendChild(btn)

        var btn = document.createElement("button");
        btn.className = "btn btn-basic";
        btn.type="button"
        btn.innerHTML = "Logs"
        div.appendChild(btn)
    }
    **/
}


/** pricefeeder Button **/
document.getElementById("pricefeeder").onclick = function(event) {
    resetActive()
    document.getElementById("pricefeeder").classList.add("active")
    //getActiveHeartbeats()
}

/** drop button **/

document.getElementById("drop").onclick = function(event) {
    resetActive()
    document.getElementById("drop").classList.add("active")
    //getActiveHeartbeats()
}

/** risk button **/
document.getElementById("risk").onclick = function(event) {
    resetActive()
    document.getElementById("risk").classList.add("active")
    //getActiveHeartbeats()
}



/** Settings Button **/
document.getElementById("settings").onclick = function() {
    resetActive()
    document.getElementById("settings").classList.add("active")
    //getActiveHeartbeats()
}



function resetActive() {
    $('#navlinks li').removeClass('active');
}

function getActiveHeartbeats() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", 'beats', true); // false for synchronous request
    xmlHttp.onload = function (err) {
        if (xmlHttp.readyState === 4) {
            if (xmlHttp.status === 200) {
                console.log(xmlHttp.responseText);

                data = JSON.parse(xmlHttp.responseText)

                document.getElementById('page').innerHTML = xmlHttp.responseText
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

function getSapphires() {
  console.log("here")
  var xmlHttp = new XMLHttpRequest();
  console.log("here again")
  xmlHttp.open("GET", 'sapphires', true);
  xmlHttp.onload = function (err) {
    if (xmlHttp.readyState === 4) {
      if (xmlHttp.status === 200) {
        console.log(xmlHttp.responseText);
        document.getElementById('page').innerHTML = xmlHttp.responseText
      }
      else {
          console.error(xmlHttp.statusText);
      }
    }
  }
  xmlHttp.onerror = function (e) {
    console.error(xmlHttp.statusText);
  };
  xmlHttp.send();
}
