class GeometriesLoader{
  static async loadForAsync(array){
    var xyzs=[]
    for (const item of array) {
      const mymol=mhchemCE.extract(item.molecule).toLowerCase().replace(" ","_")
      const myset=item.set.split("#").join("")
      try {
        const mol=await Geometry.loadXYZAsync(`/${myset}/${mymol}.xyz`)
        xyzs.push(mol)
      } catch (error) {
        console.error("Geometry not found",item)
      }
    }
    return xyzs.flat()
  }
}
