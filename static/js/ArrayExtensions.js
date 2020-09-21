if (!Array.prototype.findAsync) {
  Array.prototype.findAsync = async function findAsync(asyncCallback) {
    for (const item of this) {
      if (await asyncCallback(item)) {
        return item
      }
    }
  }
}