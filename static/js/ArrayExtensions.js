if (!Array.prototype.findAsync) {
  Array.prototype.findAsync = async function (asyncCallback) {
    for (const item of this) {
      if (await asyncCallback(item)) {
        return item
      }
    }
  }
  if (!Array.prototype.findAllIndexes) {
    Array.prototype.findAllIndexes = function (Callback) {
      this.reduce(function(a, e, i) {
        if (Callback(e))
          a.push(i)
        return a
    }, [])
    }
  }
}