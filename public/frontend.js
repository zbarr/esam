


var desks = {equities: {engines: ['es_stacker_01', 'equities_01', 'equities_02', 'equities_03', 'equities_04', 'equities_05', 'equities_06', 'equities_07']},
            cpcv: {engines: ['vmm_01', 'vmm_02', 'vmm_03']},
            bgls: {engines: ['bgls_01', 'bgls_02', 'bgls_03']},
            gas: {engines: ['gas_01', 'gas_02', 'gas_03']},
            treasuries: {engines: ['treasuries_01', 'treasuries_02']}}

var sharedServices = {drop: []}

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
document.getElementById("sidebarCollapse").onclick = function(event) {
    $('#sidebar').toggleClass('active');
    console.log("toggling")
}

document.getElementById("home").onclick = function (event) {
    resetActive()
    document.getElementById("home").classList.add("active")
}

document.getElementById("sapphires").onclick = function(event) {
    resetActive()
    document.getElementById("sapphires").classList.add("active")
    document.getElementById("grid").innerHTML = ""

    for (var i = 0; i < sapphires.length; i++) {
        var div1 = document.createElement("div");
        div1.className="col-md-4";
        document.getElementById("grid").appendChild(div1)
        var div2 = document.createElement("div");
        div2.className="panel";
        div1.appendChild(div2);
        var div3 = document.createElement("div");
        div3.className="panel-heading";
        div2.appendChild(div3);
        var div4 = document.createElement("div");
        div4.className="panel-body";
        div4.innerHTML = sapphires[i]
        div3.appendChild(div4);
    }
}

document.getElementById("ssvcs").onclick = function(event) {
    resetActive()
    document.getElementById("ssvcs").classList.add("active")
    document.getElementById("grid").innerHTML = ""
    $("#grid").innerHTML = ""
}

document.getElementById("settings").onclick = function() {
    resetActive()
    document.getElementById("settings").classList.add("active")
}



function resetActive() {
    $('#navlinks li').removeClass('active');
}


var sample = <h2>Sample</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

<div class="line"></div>

<h2>Lorem Ipsum Dolor</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

<div class="line"></div>

<h2>Lorem Ipsum Dolor</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

<div class="line"></div>

<h3>Lorem Ipsum Dolor</h3>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
