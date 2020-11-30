if (!Geometry.prototype.parseMetadata) {
  Geometry.prototype.parseMetadata = function () {
    const Ametadata = this.comment.split(",")
    const molecule = Ametadata[0]
    const stateRegExp = /^\^(\d+)(.+)$/
    const m = Ametadata[1].match(stateRegExp)
    const mul = parseInt(m[1],10)
    const sym = m[2]
    var meth = null
    if (Ametadata.length>2) {
      meth = new method(Ametadata[2],Ametadata[3])
    }
    return {
      molecule:molecule,
      multiplicity:mul,
      symmetry:sym,
      method:meth
    }
  }
}