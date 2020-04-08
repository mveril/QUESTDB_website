function numberRangeChange(e) {
  updateNumberRange(e.target)
  
}
function updateNumberRange(target) {
  var parent=target.parentElement
  var numbers=$(parent).children('input[type="number"].range')
  var min=$(numbers).filter(".min")[0]
  var max=$(numbers).filter(".max")[0]
  min.max=Number(max.value)-Number(min.step)
  max.min=Number(min.value)+Number(max.step)
}