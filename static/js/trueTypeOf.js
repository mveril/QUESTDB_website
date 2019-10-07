function trueTypeOf(object){
  result=typeof object
  if(result==typeof({})) {
    result= object.constructor.name
   }
   return result
}
