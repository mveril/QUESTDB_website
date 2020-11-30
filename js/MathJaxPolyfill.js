function MathJaxPolyfillInit(){
  if (!MathJax.typesetPromise) {
    var typesetPromise = function() {
      return new Promise(function (resolve, reject) {
        MathJax.Hub.Queue(["Typeset",MathJax.Hub],[resolve]);
      })
    }
    MathJax.typesetPromise=typesetPromise 
  }
}