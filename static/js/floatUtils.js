class stringFloat{
  constructor(value) {
    this.string=value
  }
  get Value(){
    return parseFloat(this.string)
  }
  valueOf() {
    return this.Value;
  }
  toString(){
    if (checkFloat(this.string)) {
      return this.Value
    } else {
      return this.string
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