var xmlhttp = new XMLHttpRequest();
var url = "/api/checkip";

xmlhttp.onreadystatechange = myfunction;
xmlhttp.open("GET", url, true);
xmlhttp.send(null);

function myfunction() {
    if (xmlhttp.readyState == 4) {
        //window.alert("completed");
        var y = xmlhttp.response;
        document.write(y)
    }
}