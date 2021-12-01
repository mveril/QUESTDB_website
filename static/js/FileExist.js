function FileExist(urlToFile) {
  var xhr = new XMLHttpRequest();
  xhr.open('HEAD', urlToFile, false);
  try {
    xhr.send();
  } catch (error) {
    return false
  }
  if (xhr.status == "404") {
      return false;
  } else {
      return true;
  }
}