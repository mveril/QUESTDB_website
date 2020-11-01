class indexDB {
  static async loadAsync() {
    var db = new indexDB
    const maxAge= (DebugMode.Enabled,0,600)
    const text = await getTextFromFileUrlAsync("/data/index.yaml",{"Cache-Control":`max-age=${maxAge}`})
    const myYaml = jsyaml.load(text);
    db.sets = ((myYaml.sets === null) ? new Map() : new Map(Object.entries(myYaml.sets)));
    db.others = ((myYaml.others === null) ? [] : Array.from(myYaml.others));
    return db
  }
}