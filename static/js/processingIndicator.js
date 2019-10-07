class processingIndicator{
  static get isActive(){
    return document.body.style.cursor==="wait"
  }
  static set isActive(value){
    if(value!=this.isActive){
      if(value){
        document.body.style.cursor="wait"
      }
      else{
        document.body.style.cursor="default"
      }
    }
  }
}