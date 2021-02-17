class pubUtils{
  static getIssuedDate(publi) {
    return pubUtils.parseDate(publi.issued)
  }
  static parseDate(date) {
    const parts=publi.issued["date-parts"][0]
    const [year, month, day] = date['date-parts'][0]
    if (day) {
      return new Date(Date.UTC(year, month - 1, day))
    } else if (month) {
      return new Date(Date.UTC(year, month - 1))
    } else {
      return new Date(Date.UTC(year))
    }
  }
}