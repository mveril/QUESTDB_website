async function loadAllData() {
  dic = {
    abs: [],
    fluo: [],
    ZPE: []
  };
  dic.abs = await Promise.all(getAbsFilesName().map((f) => VertDataFile.loadAsync(f,VertExcitationKinds.Absorbtion)))
  dic.fluo = await Promise.all(getFluoFilesName().map((f) => VertDataFile.loadAsync(f,VertExcitationKinds.Fluorescence)))
  return dic;
}
