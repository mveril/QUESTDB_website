function getjsonfromfile(path) {
  var result = null;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp
  xmlhttp.open("GET", path, false);
  xmlhttp.send();
  if (xmlhttp.status==200) {
    text = xmlhttp.responseText;
  }
  return JSON.parse(text);
}
function getdoiurl(datas) {
  return 'https://doi.org/'+datas.doi
}
function getdoiurlfromfile(file) {
  return getdoiurl(getjsonfromfile('datas/'+file))
}