var xmlhttp = new XMLHttpRequest();

function doFunction(parameters) {
    let toFind = parameters;
    xmlhttp.open("POST", "/find");
    var e = document.getElementById("myData");

    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    var div = document.createElement("div");
    div.classList.add("loader");
    e.appendChild(div);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify(toFind));

}

xmlhttp.onreadystatechange = function() {
if (this.readyState == 4 && this.status == 200) {
        var e = document.getElementById("myData").innerText = "";

        var child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }
        var myArr = JSON.parse(this.responseText);
        var mainContainer = document.getElementById("myData");
        if (myArr['street'].length > 0) {
            for (var i = 0; i < myArr['street'].length; i++) {
                var div = document.createElement("div");
                div.innerHTML = 'Street: ' + myArr['street'][i]['name'] +"<br>";
                div.innerHTML += 'Possibility: ' + myArr['street'][i]['token'];
                mainContainer.appendChild(div);
            }
        } else {
            var div = document.createElement("div");
            div.innerHTML += "Sorry, your input doesn't match any of our records.";
            mainContainer.appendChild(div);
        }
    }
};
