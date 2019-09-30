class websiteFile{
  constructor(path){
    this.path=path
  }
  get viewerUrl(){
    return String.raw`/view?dataFile=${this.path}`
  }
}