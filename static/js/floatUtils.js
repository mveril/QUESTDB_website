class stringFloat{
  constructor(value,printNaN=true) {
    this.string=value
    this.printNaN=printNaN
  }
  get Value(){
    return parseFloat(this.string)
  }
  valueOf() {
    return this.Value;
  }
  toString(){
    if (checkFloat(this.string) && this.printNaN) {
      return this.string
    } else {
      return NaN.toString()
    }
  }
}
function checkFloat(string) {
  try {
    return !isNaN(parseFloat(string))
  } catch (error) {
    return false
  }
}