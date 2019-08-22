function getDataFromFile(file) {
  var result = null;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp
  xmlhttp.open("GET",getFullDataPath(file), false);
  xmlhttp.send();
  if (xmlhttp.status==200) {
    text = xmlhttp.responseText;
  }
  return JSON.parse(text);
}

function getDoiUrl(data) {
  return 'https://doi.org/'+data.doi
}
function getFullDataPath(path) {
  return 'data/'+path
}
