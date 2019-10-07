async function loadAllData() {
  dic = {
    abs: [],
    fluo: [],
    ZPE: []
  };
  dic.abs = await Promise.all(getAbsFilesName().map((f) => AbsDataFile.loadAsync(f)))
  dic.fluo = await Promise.all(getFluoFilesName().map((f) => FluoDataFile.loadAsync(f)))
  dic.ZPE = await Promise.all(getZPEFilesName().map((f) => ZPEDataFile.loadAsync(f)));
  return dic;
}
