function checkFloat(string) {
  try {
    return isNaN(parseFloat(string))
  } catch (error) {
    return false
  }
}