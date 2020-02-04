class stringNumber{
  constructor(value,printNaN=true) {
    this.string=value
    this.printNaN=printNaN
  }
  valueOf() {
    return parseFloat(this.string)
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