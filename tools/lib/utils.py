import itertools
import sys
from TexSoup import TexEnv,TexNode, RArg
from collections.abc import Iterable
def nodify(TexArray,envName="[tex]",parent=None):  
  env=TexEnv(envName,TexArray)
  node=TexNode(env)
  node.parent=parent
  return node
def desarg(tex):
  lst=[]
  for item in tex.contents:
    if type(item) is RArg:
      myitem=item.contents
      if type(myitem) is list:
        for myit in myitem:
          lst.append(myit)
      else:
        lst.append(myit)
    else:
      myitem=item      
      lst.append(myitem)  
  return nodify(lst,tex.name,tex.parent)
def getValFromCell(cell):
    unsafe=False
    val= list(cell.contents)[0]
    if type(val) is TexNode and val.name=='emph':
      unsafe=True
      val=val.string
      val=toFloat(str(val))
    return (val,unsafe)

def toFloat(x):
  try:
    return float(x)
  except ValueError:
    return None