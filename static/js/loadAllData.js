async function loadAllData() {
  dic = {
    abs: [],
    fluo: [],
  };
  for (const f of getAbsFilesName()) {
    dic.abs.push(await VertDataFile.loadAsync(f,VertExcitationKinds.Absorbtion))
  }
  for (const f of getFluoFilesName()) {
    dic.fluo.push(await VertDataFile.loadAsync(f,VertExcitationKinds.Fluorescence))
  }
  return dic;
}
