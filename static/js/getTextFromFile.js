async function getTextFromFileUrlAsync(url) {
  return new Promise(function (resolve, reject) {
  var req = new XMLHttpRequest();
  req.open("GET",url, true);
  for (const item of ["no-cache","no-store","must-revalidate"]) {
    req.setRequestHeader("Cache-Control",item)
  }
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

async function getTextFromUploadedFileAsync(inputFile){
  const temporaryFileReader = new FileReader();

  return new Promise((resolve, reject) => {
    temporaryFileReader.onerror = () => {
      temporaryFileReader.abort();
      reject(new DOMException("Problem parsing input file."));
    };

    temporaryFileReader.onload = () => {
      resolve(temporaryFileReader.result);
    };
    temporaryFileReader.readAsText(inputFile);
  });
};