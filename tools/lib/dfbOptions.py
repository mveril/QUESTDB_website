from TexSoup import TexSoup,TexCmd
from . import formats
from .data import dataFileBase,DataType,state
from collections import defaultdict

class dfbOptions(object):
  def __init__(self):
    self.defaultType=DataType.ABS
    self.format="line"
    self.suffix=None
    self.initialStates=defaultdict(lambda : state(1,1,"A_1"))
    self.isDouble=False
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
    dfbIsDouble=lateEnv.isDouble
    if dfbIsDouble!=None:
      dfbIsDouble=dfbIsDouble.expr
      if type(dfbIsDouble) is TexCmd:
        if len(dfbIsDouble.args)==0:
          dfb_Opt.isDouble = True
        elif len(dfbIsDouble.args)==1 and dfbIsDouble.args[0].type=="optional":
          isDoubleStr=dfbIsDouble.args[0].value
          if isDoubleStr == "true":
            dfb_Opt.isDouble = True
          elif isDoubleStr == "false":
            isDouble = False
          else:
            raise ValueError("\isDouble must be 'true' or 'false'.")
        else:
          raise ValueError("Arguments error on '\isDouble'. Only one optional argument is supported.")
    return dfb_Opt