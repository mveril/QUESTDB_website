class stringNumber{
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
    if (checkNumber(this.string) && this.printNaN) {
      return this.string
    } else {
      return NaN.toString()
    }
  }
}
function checkNumber(string) {
  try {
    return !Number.isNaN(parseFloat(string))
  } catch (error) {
    return false
  }
}