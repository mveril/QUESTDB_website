async function getTextFromFileAsync(file) {
  return new Promise(function (resolve, reject) {
  var req = new XMLHttpRequest();
  req.open("GET",file, true);
  req.onreadystatechange = function() {
    if (req.readyState == 4) {
      if (req.status == 200) {//when a good response is given do this
        var text = req.responseText;
        resolve(text);
      } else {
        reject({
          status: req.status,
          statusText: req.statusText
        });
      }
    }
  }
  req.send();
  });
}