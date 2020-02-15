async function getPublis() {
  const text = await getTextFromFileUrlAsync("/data/publis.yaml")
  const myYaml=jsyaml.load(text);
  myYaml.sets= ((myYaml.sets===null) ? new Map() : new Map(Object.entries(myYaml.sets)));
  myYaml.others=((myYaml.others===null) ? new Map() : new Map(Object.entries(myYaml.others)));
  return myYaml
}