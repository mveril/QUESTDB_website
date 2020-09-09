class publiDB {
  static async loadAsync() {
    var db = new publiDB
    const text = await getTextFromFileUrlAsync("/data/publis/index.yaml")
    const myYaml = jsyaml.load(text);
    db.sets = ((myYaml.sets === null) ? new Map() : new Map(Object.entries(myYaml.sets)));
    db.others = ((myYaml.others === null) ? new Map() : new Map(Object.entries(myYaml.others)));
    return db
  }
  static get UnknowSetName() {
    return "Unknow set"
  }
  findNameFromSet(set, supportUnknow = false) {
    if (supportUnknow && JSON.stringify(set) === JSON.stringify([""])) {
      return publiDB.UnknowSetName
    }
    for (let [setname, articles] of this.sets.entries()) {
      if (JSON.stringify(set.sort()) === JSON.stringify(articles.sort())) {
        return setname
      }
    }
    return null
  }
  findSetNameFromArticle(article, supportUnknow = false) {
    for (let [setname, articles] of this.sets.entries()) {
      if (articles.includes(article))
        return setname
    }
    if (supportUnknow && article === "") {
      return publiDB.UnknowSetName
    }
    return null
  }
}