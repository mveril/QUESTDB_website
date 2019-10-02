class websiteFile{
  constructor(file){
    this.file=file
  }

  async getViewerURL(){
    var urlbase="/view"
    switch (trueTypeOf(this.file)) {
      case "string":
        return String.raw`${urlbase}?file=${this.file}`
        break
      case "File":
        var base64=btoa(await getTextFromUploadedFileAsync(this.file))
        return String.raw`${urlbase}?fileBase64=${base64}`;
        break
    }
  }
}