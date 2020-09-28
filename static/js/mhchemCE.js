class mhchemCE{
  static extract(string) {
    const m = string.match(mhchemCE.regEx)
    if (m) {
      return m[1]
    } else {
      return string
    }
  }
  static test(string){
    return mhchemCE.regEx.test(string)
  }
  static get regEx(){
    return /^\\ce\{(.*)\}$/
  }
}
