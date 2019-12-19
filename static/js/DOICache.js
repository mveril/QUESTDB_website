class DOICache{
  constructor(){
  this._doimap=new Map()
  this._Cite=require("citation-js")
  }
  clear(){
    this._doimap.clear()
  }
  delete(doi){
    return this._doimap.delete(doi)
  }
  forEach(callbackfn, thisArg=None){
    return this._doimap.forEach(callbackfn,thisArg)
  }
  get(doi){
    return this._doimap.get(doi)
  }
  has(doi){
    return this._doimap.has(doi)
  }
  async add(doi){
    if(!this.has(doi)){
      const publi=await this._Cite.async(doi)
      this._doimap.set(doi,publi)
    }
  }
  async addRange(dois){
    const set=new Set(dois)
    for(const doi of set){
     await this.add(doi)
    }
  }
  get size(){
    return this._doimap.size()
  }
  keys() { return this._doimap.keys()}
  values() { return this._doimap.values()}
  entries() { return this._doimap.entries()}
  [Symbol.iterator]() { return this.values()}
}