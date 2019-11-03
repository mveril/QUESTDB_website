class QueryUpdater{
  static set(key,value){
    var url=new URL(window.location.href)
    var params=url.searchParams
    params.set(key,value)
    window.history.pushState('', '', url.href)
  }
  static delete(key){
    var url=new URL(window.location.href)
    var params=url.searchParams
    params.delete(key)
    window.history.pushState('', '', url.href)
  }
}