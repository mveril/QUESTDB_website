function getDataFromFile(file,fn) {
  var result = null;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp
  xmlhttp.open("GET",getFullDataPath(file), true);
  xmlhttp.onreadystatechange = function() { 
    if (this.readyState == 4 && this.status == 200) {//when a good response is given do this

        var data = JSON.parse(this.responseText); // convert the response to a json object
        fn(data)
    }
  }
  xmlhttp.send();
}

function getDoiUrl(data) {
  return 'https://doi.org/'+data.doi
}
function getFullDataPath(path) {
  return 'data/'+path
}
