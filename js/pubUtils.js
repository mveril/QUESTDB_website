class pubUtils{
  static getIssuedDate(publi) {
    const parts=publi.issued["date-parts"][0]
    return new Date(Date.UTC(parts[0], parts[1] - 1, parts[2]))
  }
}