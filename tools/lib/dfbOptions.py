from TexSoup import TexSoup
from TexSoup.data import TexCmd
from . import formats
from .data import dataFileBase,DataType,state
from collections import defaultdict

class dfbOptions(object):
  def __init__(self):
    self.defaultType=DataType.ABS
    self.format="line"
    self.suffix=None
    self.initialStates=defaultdict(lambda : state(1,1,"A_1"))
    
  @staticmethod
  def readFromEnv(lateEnv):
    dfb_Opt=dfbOptions()
    dfbDefaultTypeNode=lateEnv.defaultType
    if dfbDefaultTypeNode!=None:
      dfbDefaultType=dfbDefaultTypeNode.expr
      if type(dfbDefaultType) is TexCmd:
        dfb_Opt.defaultType=DataType[dfbDefaultType.args[0].value.upper()]

    dfbFormatNode=lateEnv.format
    if dfbFormatNode!=None:
      dfbFormat=dfbFormatNode.expr
      if type(dfbFormat) is TexCmd:
        dfb_Opt.format=dfbFormat.args[0].value

    dfbSuffixNode=lateEnv.suffix
    if dfbSuffixNode!=None:
      dfbSuffix=dfbSuffixNode.expr
      if type(dfbSuffix) is TexCmd:
        dfb_Opt.suffix=dfbSuffix.args[0].value
    dfbInitialStateNodes=list(lateEnv.find_all("initialState"))
    for node in dfbInitialStateNodes:
      initialState=node.expr
      if type(initialState) is TexCmd:
        vRArgs=[arg.value for arg in initialState.args if arg.type=="required"]
        vOArgs=[arg.value for arg in initialState.args if arg.type=="optional"]
        if len(vOArgs)==0:
          defaultstate=state.fromString("1 "+vRArgs[0])
          dfb_Opt.initialStates.default_factory=lambda : defaultstate
        else:
          mystate=state.fromString("1 "+vRArgs[0])
          dfb_Opt.initialStates[vOArgs[0]]=mystate
    return dfb_Opt    