function trueTypeOf(object){
  if (object==null){
    return "null"
  }
  else {
   return object.constructor.name
  }
}
