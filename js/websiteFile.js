class websiteFile{
  constructor(file){
    this.file=file
  }

  async getViewerURL(){
    var params=new URLSearchParams()
    var urlbase="/view"
    switch (trueTypeOf(this.file)) {
      case String.name:
        params.append("file",this.file)
        break
      case File.name:
        var base64=btoa(await getTextFromUploadedFileAsync(this.file))
        params.append("fileBase64",base64);
        break
    }
    if ([...params].length>0){
      return urlbase+"?"+params.toString()
    }
    else{
      return urlbase   
    }
      
  }
}