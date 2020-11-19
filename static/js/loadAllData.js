async function loadAllData() {
  dic = {
    abs: [],
    fluo: [],
  };
  for (const f of getAbsFilesName()) {
//    dic.abs.push(VertDataFile.load(f,VertExcitationKinds.Absorbtion))
    dic.abs.push(await VertDataFile.loadAsync(f,VertExcitationKinds.Absorbtion))
  }
  for (const f of getFluoFilesName()) {
//    dic.fluo.push(VertDataFile.load(f,VertExcitationKinds.Fluorescence))
    dic.fluo.push(await VertDataFile.loadAsync(f,VertExcitationKinds.Fluorescence))
  }
  return dic;
}
