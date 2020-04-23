class MathJaxUtils {
  static get start(){
    return '\\('
  }
  static get end(){
    return '\\)'
  }
  static getMathJaxString(string){
    return MathJaxUtils.start+string+MathJaxUtils.end
  }
}