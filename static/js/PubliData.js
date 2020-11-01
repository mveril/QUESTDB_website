class PubliData{
  static async loadAsync(DOI){
    const path = PubliData.GetPathForDOI(DOI)
    var me = JSON.parse(await getTextFromFileUrlAsync(`${path}/metadata.json`))
    Reflect.setPrototypeOf(me,PubliData.prototype)
    return me
  }
  static async loadManyAsync(DOIs){
    var data = []
    for (const DOI of DOIs) {
      if (DOI!=null) {
        data.push(await PubliData.loadAsync(DOI))
      }
    }
    return data
  }
  get Path(){
    return PubliData.GetPathForDOI(this.DOI)
  }
  get PictureURL(){
    return PubliData.GetPictureURLForDOI(this.DOI)
  }
  get AbstractURL(){
    return PubliData.GetAbstractURLForDOI(this.DOI)
  }
  async getAbstractTextAsync(){
    return await PubliData.getAbstractTexForDOIAsync(this.DOI)
  }

  static GetPathForDOI(DOI){
    return `/data/publis/${DOI.replaceAll(".","/")}`
  }
  static GetAbstractURLForDOI(DOI){
    return `${PubliData.GetPathForDOI(DOI)}/abstract.html`
  }

  static GetPictureURLForDOI(DOI){
    return `${PubliData.GetPathForDOI(DOI)}/picture.jpeg`
  }

  static async getAbstractTexForDOIAsync(DOI){
    return await getTextFromFileUrlAsync(PubliData.GetAbstractURLForDOI(DOI))
  }
}