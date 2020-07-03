from ..formatHandlerBase import formatHandlerBase
from ..formatName import formatName
from ...data import dataFileBase,DataType,method,excitationValue,datafileSelector,getSubtableIndex
from ...utils import getValFromCell
@formatName("column")
class columnHandler(formatHandlerBase):
  def readFromTable(self,table):
    datalist=list()
    subtablesindex=getSubtableIndex(table)
    for first, last in subtablesindex:
      for col in range(2,np.size(table,1)):
        datacls=dict()
        col=table[:,col]
        mymolecule=str(table[first,0])
        initialState=TexOps.initialStates[mymolecule]
        mymethod=method(str(col[1]),str(col[0]))
        finsts=dataFileBase.convertState(table[first:last+1,1],initialState,default=TexOps.defaultType,commands=commands)
        for index,cell in enumerate(col[first:last+1]):
          if str(cell)!="":
            val,unsafe=getValFromCell(cell)
            finst=finsts[index]
            dt=finst[1]
            if dt in datacls:
              data=datacls[dt]
            else:
              cl=datafileSelector[dt]
              data=cl()
              data.molecule=mymolecule
              data.method=mymethod
              datacls[dt]=data
            data.excitations.append(excitationValue(initialState,finst[0],val,type=finst[2]))
        for value in datacls.values():
          datalist.append(value)
    return datalist