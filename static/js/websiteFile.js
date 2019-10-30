class websiteFile{
  constructor(file){
    this.file=file
  }

  async getViewerURL(){
    params=new URLSearchParams()
    var urlbase="/view"
    switch (trueTypeOf(this.file)) {
      case "string":
        params.append("file",this.file)
        break
      case "File":
        var base64=btoa(await getTextFromUploadedFileAsync(this.file))
        params.append("fileBase64",base64);
        break
    }
    if ([...params].length>0){
      return urlbase+"?"+params.tostring()
    }
    else{
      return urlbase   
    }
      
  }
}