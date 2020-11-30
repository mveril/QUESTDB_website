function base64ToBlob(Base64String,type="") {
  byteString=atob(Base64String)
  var ab = new ArrayBuffer(byteString.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }

  // write the ArrayBuffer to a blob, and you're done
  var bb=null
  if (type=="") {
    var bb = new Blob([ab]);
  }
  else {
    var bb = new Blob([ab], {type : type});
  }
  return bb;
}
