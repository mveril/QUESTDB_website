class indexDB {
  static async loadAsync() {
    var db = new indexDB
    const text = await getTextFromFileUrlAsync("/data/index.yaml")
    const myYaml = jsyaml.load(text);
    db.sets = ((myYaml.sets === null) ? new Map() : new Map(Object.entries(myYaml.sets)));
    db.others = ((myYaml.others === null) ? [] : Array.from(myYaml.others));
    return db
  }
}