from abc import ABCMeta
from os import stat
from TexSoup import TexSoup
from ..formatHandlerBase import formatHandlerBase
from ..formatName import formatName
from ...data import AbsDataFile, dataFileBase,DataType,method,excitationValue,getSubtablesRange,state
from ...utils import getValFromCell
from ...LaTeX import newCommand
import numpy as np

class CTFormatHandlerBase(formatHandlerBase, metaclass=ABCMeta):
  def __init__(self, TexOps,usedefaultBasis, commands=None):
      super().__init__(TexOps, commands=commands)
      self.__usedefaultBasis=usedefaultBasis
  def __ParseState(self,stateSoup):
    contents=list(stateSoup)
    num=int(str(contents[0]).strip())
    symmnode=contents[1]
    if symmnode.expr.name=="$":
      newCommand.runAll(symmnode,self.Commands)
      return state(num,1,symmnode.string)
  def _readFromTableCore(self,table):
    datalist=list()
    subtablesRange=getSubtablesRange(table,firstindex=1 if self.__usedefaultBasis else 2)
    for myrange in subtablesRange:
      for col in range(2,np.size(table,1)):
        col=table[:,col]
        mymolecule=str(table[myrange[0],0])
        initialState=self.TexOps.initialStates[mymolecule]
        mymethod=method(str(col[0]),self.TexOps.defaultBasis) if self.__usedefaultBasis else method(str(col[1]),str(col[0])) 
        data=AbsDataFile()
        data.molecule=mymolecule
        data.method=mymethod
        for index,cell in enumerate(col[myrange]):
          if str(cell)!="":
            val,unsafe=getValFromCell(cell)
            state=self.__ParseState(table[myrange[0]+index,1])            
            data.excitations.append(excitationValue(initialState,state,val,type=r"\mathrm{CT}"))
        if len(data.excitations)>0:
          datalist.append(data)
    return datalist

@formatName("CT1")
class CT1Handler(CTFormatHandlerBase):
  def __init__(self, TexOps, commands=None):
      super().__init__(TexOps, False, commands=commands)

@formatName("CT2")
class CT2Handler(CTFormatHandlerBase):
  def __init__(self, TexOps, commands=None):
      super().__init__(TexOps, True, commands=commands)