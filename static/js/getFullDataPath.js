function getFullDataPath(path) {
  var site_url = "/"+window.location.pathname.split('/')[1];
  return site_url+'/data/' + path;
}
