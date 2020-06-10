class DebugMode {
  static get Enabled() {
    var debug = window.sessionStorage.getItem("debug")
    if (debug == null) {
      return false
    }
    else {
      return Boolean(JSON.parse(debug))
    }
  }

  static set Enabled(value) {
    const newval = Boolean(value)
    if (this.Enabled !== newval) {
      window.sessionStorage.setItem("debug", newval)
      window.location.reload()
    }
  }
}