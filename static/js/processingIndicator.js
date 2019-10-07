class processingIndicator{
  static get isActive(){
    return document.body.classList.contains("loading")
  }
  static set isActive(value){
    if(value!=this.isActive){
      if(value){
        document.body.classList.add("loading")
      }
      else{
        document.body.classList.remove("loading")
      }
    }
  }
}