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
      return this.reduce(function(a, e, i) {
        if (Callback(e))
          a.push(i)
        return a
    }, [])
    }
  }
  if (!Array.prototype.count) {
    Array.prototype.count = function (o) {
      var callback
      var item
      if (typeof o==="function") {
        callback=o
      }
      else {
        callback=(e)=>item==e
      }
      return this.reduce(function(c, e, i) {
        if (callback) {
          if (callback(e))
            c++
          return c
        }
    },0)
    }
  }
}