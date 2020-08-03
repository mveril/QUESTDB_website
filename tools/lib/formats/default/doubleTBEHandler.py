from ..formatHandlerBase import formatHandlerBase
from ..formatName import formatName
from ...data import dataFileBase,DataType,method,excitationValue,datafileSelector,getSubtablesRange,AbsDataFile,state
from ...utils import getValFromCell, checkFloat
from ...LaTeX import newCommand
from TexSoup import TexSoup
import re
@formatName("doubleTBE")
class doubleTBEHandler(formatHandlerBase):
  def readFromTable(self,table):
    datalist=list()
    subtablesMol=getSubtablesRange(table)
    for rangeMol in subtablesMol:
      data=AbsDataFile()
      data.molecule=str(table[rangeMol[0],0])
      data.method=method("TBE","CBS")
      for mytrans in table[rangeMol]:
        try:
          mathsoup=TexSoup(mytrans[1])
        except:
          print(f"Error when parsing latex state: {str(mytransdesc[i])}")
          exit(-1)
        newCommand.runAll(mathsoup,self.commands)
        mytransdesc=str(mathsoup)
        infin=mytransdesc.split(r"\rightarrow")
        for i,item in enumerate(infin):
          m=re.match(r"^(?P<number>\d)\\[,:;\s]\s*\^(?P<multiplicity>\d)(?P<sym>\S*)",item.strip())
          infin[i]=state(m.group("number"),m.group("multiplicity"),m.group("sym"))
        cell=mytrans[6]
        val,unsafe=getValFromCell(cell)
        data.excitations.append(excitationValue(infin[0],infin[1],val,isUnsafe=unsafe))
      datalist.append(data)
    return datalist