async function loadAllData() {
  dic = {
    abs: [],
    fluo: [],
  };
  for (const f of getAbsFilesName()) {
    dic.abs.push(VertDataFile.load(f,VertExcitationKinds.Absorbtion))
  }
  for (const f of getFluoFilesName()) {
    dic.fluo.push(VertDataFile.load(f,VertExcitationKinds.Fluorescence))
  }
  return dic;
}
