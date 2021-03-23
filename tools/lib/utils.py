import itertools
import sys
from TexSoup.data import TexEnv,TexNode, BraceGroup
from collections.abc import Iterable
def nodify(TexArray,envName="[tex]",parent=None):  
  env=TexEnv(envName,"","",TexArray)
  node=TexNode(env)
  node.parent=parent
  return node
def desarg(tex):
  lst=[]
  for item in tex.contents:
    if type(item) is BraceGroup:
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
    lst= list(cell.contents)
    val= lst[0]
    if type(val) is TexNode and str(val.expr)=='$\sim$' :
      unsafe=True
      val = lst[1]
      val=checkFloat(str(val))
    elif type(val) is TexNode and val.name=='emph':
      unsafe=True
      val=val.string
      val=checkFloat(str(val))
    return (val,unsafe)

def checkFloat(x):
  try:
    float(x)
    return x
  except ValueError:
    return None