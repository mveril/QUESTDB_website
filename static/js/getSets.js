async function getSets(){
  var m=new Map()
  const text=await getTextFromFileUrlAsync("/data/datasets.lst")
  const lines=text.split("\n")
  for(const line of lines){
    const kv=line.split(":",2)
    m.set(kv[0].trim(),kv[1].trim())
  }
  return m
}