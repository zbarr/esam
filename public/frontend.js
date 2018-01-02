var desks = {'equities':{engines:['es_stacker_01', 'equities_01', 'equities_02', 'equities_03', 'equities_04', 'equities_05', 'equities_06', 'equities_07']},
            'CPCV': {engines: ['vmm_01', 'vmm_02', 'vmm_03']},
            'bgls': {engines: ['bgls_01', 'bgls_02', 'bgls_03']},
            'gas': {engines: ['gas_01', 'gas_02', 'gas_03']},
            'treasuries': {engines: ['treasuries_01', 'treasuries_02']}}




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
}

document.getElementById("ssvcs").onclick = function(event) {
    resetActive()
    document.getElementById("ssvcs").classList.add("active")
}

document.getElementById("settings").onclick = function() {
    resetActive()
    document.getElementById("settings").classList.add("active")
}



function resetActive() {
    $('#navlinks li').removeClass('active');
}
