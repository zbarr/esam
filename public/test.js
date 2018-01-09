<li>
    <div class="container-fluid">
        <ul id="sidebar-section" class="nav navbar-nav">
            <li>
                <a id="desk" href="#">equities</a>
                <ul class="collapse list-unstyled" id="homeSubmenu">
                    <li><a href"#">equities_01</a></li>
                    <li><a href"#">equities_02</a></li>
                    <li><a href"#">equities_03</a></li>
                </ul>
            </li>
        </ul>
        <ul id="arrow" class="nav navbar-nav navbar-right"
            <li><a href="#homeSubmenu" data-toggle="collapse" aria-expanded="false"><span class="glyphicon glyphicon-menu-down"></a></li>
        </ul>
    </div>
</li>
<li><a href="#">CPCV</a></li>
<li>
    <a href="#homeSubmenu2" data-toggle="collapse" aria-expanded="false">bgls</a>
    <ul class="collapse list-unstyled" id="homeSubmenu2">
        <li><a href"#">bgls_01</a></li>
        <li><a href"#">bgls_02</a></li>
        <li><a href"#">bgls_03</a></li>
    </ul>
</li>
<li><a href="#">gas</a></li>
<li><a href="#">treasuries</a></li>


/**
strings = topic.toString()
console.log(strings)
replaced = strings.replace(" ", "")
console.log(replaced)
splitted = replaced.split('\n')
console.log(splitted)

**/
data = topic.replace(" ", "").toString().split('\n')


<h2>Sample</h2>
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





//getActiveHeartbeats()


/** Sidebar **/
//document.getElementById("sidebar-items").innerHTML=""

for (desk in desks) {

    var li = document.createElement("li")
    document.getElementById("sidebar-items").appendChild(li)

    var div = document.createElement("div")
    div.className = "container-fluid"
    li.appendChild(div)

    var ul = document.createElement("ul")
    ul.id = "sidebar-section"
    ul.className = "nav navbar-nav"
    div.appendChild(ul)

    var li = document.createElement("li")
    ul.appendChild(li)

    var a = document.createElement("a")
    a.id = "desk"
    a.href = "#"
    a.innerHTML = desk
    li.appendChild(a)

    var ul = document.createElement("ul")
    ul.className = "collapse list-unstyled"
    ul.id = desk
    li.appendChild(ul)

    for (var i = 0; i < desks[desk].engines.length; i++) {
        var li = document.createElement("li")
        ul.appendChild(li)
        var a = document.createElement("a")
        a.href="#"
        a.id = "engine"
        a.innerHTML = desks[desk].engines[i]
        li.appendChild(a)
    }


    //Arrow stuff
    var ul = document.createElement("ul")
    ul.id = "arrow"
    ul.className = "nav navbar-nav navbar-right"
    div.appendChild(ul)

    var li = document.createElement("li")
    li.innerHTML = '<a href="#' + desk + '" data-toggle="collapse" aria-expanded="false"><i class="glyphicon glyphicon-menu-down"></i><i class="glyphicon glyphicon-menu-up"></i>'
    ul.appendChild(li)
    //End arrow stuff
}
