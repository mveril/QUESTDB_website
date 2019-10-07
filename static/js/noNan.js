function noNanPrecision(number,precision)
{
  if(Number.isNaN(number)){
    return ""
  }
  else {
    return number.toPrecision(precision)
  }
}

function noNanFixed(number,precision)
{
  if(Number.isNaN(number)){
    return ""
  }
  else {
    return number.toFixed(precision)
  }
}