from collections import OrderedDict
from TexSoup import TexSoup
from .LaTeX import newCommand
from .utils import getValFromCell,checkFloat
from TexSoup import TexNode,TexEnv
from enum import IntEnum,auto,unique,IntFlag
from .formats import getFormatHandlers
import re
import numpy as np
import json

class state:
  def __init__(self,number, multiplicity, symetry):
    self.number = number
    self.multiplicity = multiplicity
    self.symetry = symetry
  @staticmethod
  def fromString(string):
    m=re.match(r"^(?P<number>\d)\s*\^(?P<multiplicity>\d)(?P<sym>\S*)",string)
    num=m.group('number')
    mul=m.group('multiplicity')
    sym=m.group('sym')
    return state(num,mul,sym)
@unique
class DataType(IntEnum):
  ABS=auto()
  FLUO=auto()
  
def datafileSelector(dataType):
  switcher={
    DataType.ABS:AbsDataFile,
    DataType.FLUO:FluoDataFile,
  }
  return switcher[dataType]

def getSubtableIndex(table,firstindex=2,column=0,count=1):
  subtablesindex=list()
  i=firstindex+count
  while i<np.size(table,0):
    if str(table[i,column])!="":
      subtablesindex.append((firstindex,i-1))
      firstindex=i
      i+=count
    else:
      i+=1
  subtablesindex.append((firstindex,np.size(table,0)))
  return subtablesindex

class dataFileBase(object):
  def __init__(self):
    self.molecule = ''
    self.comment = ''
    self.code = None
    self.method = None
    self.excitations = []
    self.DOI = ''

  @property
  def IsTBE(self):
    return self.method.name=="TBE"

  @staticmethod
  def GetFileType():
    pass

  @staticmethod
  def convertState(StateTablelist,initialState,default=DataType.ABS,commands=[]):
    tmplst=[]
    for TexState in StateTablelist:
      math=TexState.find("$")
      lst=list(math.contents)
      mystr=str(lst[0])
      mathsoup=None
      try:
        mathsoup=TexSoup(mystr)
      except:
        print(f"Error when parsing latex state: {mystr}")
        exit(-1)
      newCommand.runAll(mathsoup,commands)
      st=str(mathsoup)
      m=re.match(r"^\^(?P<multiplicity>\d)(?P<symm>[^\s\[(]*)\s*(?:\[(?:\\mathrm{)?(?P<special>\w)(?:})\])?\s*(:?\((?P<type>[^\)]*)\))?",st)
      seq=m.group("multiplicity","symm")
      mul=int(m.group("multiplicity"))
      symm=m.group("symm")
      spgrp=m.group("special")
      if spgrp is not None and spgrp=="F":
        trsp=DataType.FLUO
      else:
        trsp=default
      tygrp=m.group("type")
      tmplst.append((mul,symm,trsp,tygrp))
    lst=[]
    for index,item in enumerate(tmplst):
      unforminitialstate=(initialState.multiplicity,initialState.symetry)
      countlst=[unforminitialstate]+[(it[0],it[1]) for it in tmplst[:index+1]]
      countitem=(item[0],item[1])
      count=countlst.count(countitem)
      lst.append((state(count,item[0],item[1]),item[2],item[3]))
    return lst
  @staticmethod
  def readFromTable(table,TexOps, commands=[]):
    for formatName,Cls in getFormatHandlers:
      if formatName.lower()==TexOps.format.lower():
        handler=Cls(TexOps,commands)
        break
    else:
      raise ValueError()
    return handler.readFromTable(table)
  def getMetadata(self):
    dic=OrderedDict()
    dic["Molecule"]=self.molecule
    dic["Comment"]=self.comment
    dic["code"]="" if self.code is None else self.code.toDataString()
    dic["method"]="" if self.method is None else self.method.toDataString()
    dic["DOI"]="" if self.DOI is None else self.DOI
    return dic
  
  def toFile(self,datadir,suffix=None):
    subpath=datadir/self.GetFileType().name.lower()
    if not subpath.exists():
      subpath.mkdir()
    molsoup=TexSoup(self.molecule)
    molcomp=list(molsoup.contents)[0]
    molfilename=self.molecule if isinstance(molcomp,str) else molcomp.args[0].value
    molfilename=molfilename.lower().replace(" ","_")
    fileNameComp=[molfilename,self.method.name]
    if self.method.basis:
      fileNameComp.append(self.method.basis)
    if suffix:
      fileNameComp.append(suffix)
    fileName="_".join(fileNameComp)+".dat"
    file=subpath/fileName
    if not file.exists():
      with file.open("w") as f:
        for key,value in self.getMetadata().items():
          if value is not None:
            f.write("# {:9s}: {}\n".format(key,value))
        f.write("""
# Initial state            Final state                        Transition                    Energies (eV)   %T1    Oscilator forces     unsafe
#######################  #######################  ########################################  ############# ####### ################### ##############
# Number  Spin  Symm       Number  Spin  Symm         type                                    E_{:5s}       %T1            f            is unsafe\n""".format(self.GetFileType().name.lower()))
        for ex in self.excitations:
          mystr="  {:7s} {:5s} {:10s} {:7s} {:5s} {:12s} {:39s} {:13s} {:14s} {:13s}{}\n".format(
            str(ex.initial.number),
            str(ex.initial.multiplicity),
            ex.initial.symetry,
            str(ex.final.number),
            str(ex.final.multiplicity),
            ex.final.symetry,"("+str(ex.type)+")" if ex.type is not None else "_",
            str(ex.value) if ex.value is not None else "_",
            str(ex.T1) if ex.T1 is not None else "_",
            str(ex.oscilatorForces) if ex.oscilatorForces is not None else "_",
            json.dumps(ex.isUnsafe))
          f.write(mystr)
class method:
  def __init__(self,name, *args):
    self.name = name
    self.basis=args[0] if len(args)>0 else None

  @staticmethod
  def fromString(string):
    vals = string.split(",")
    return method(*vals)


  def __str__(self):
    string = self.name
    if (self.basis):
      string+= '/' + self.basis
    return string

  def toDataString(self):
    string=self.name
    if (self.basis):
      string+=","+self.basis
    return string

class code:
  def __init__(self,name, version):
    self.name = name
    self.version = version
  
  def toDataString(self):
    string=self.name
    if (self.version):
      string+=","+self.version
    return string
  
class oneStateDataFileBase(dataFileBase):
  def __init__(self):
    super(oneStateDataFileBase,self).__init__()
    self.geometry = None
  
  def getMetadata(self):
    dic=super(oneStateDataFileBase,self).getMetadata()
    dic["geom"]= "" if self.geometry is None else self.geometry.toDataString()
    dic.move_to_end("DOI")
    return dic

class AbsDataFile(oneStateDataFileBase):
  def __init__(self):
    super(AbsDataFile,self).__init__()
  
  @staticmethod
  def GetFileType():
    return DataType.ABS

class FluoDataFile(oneStateDataFileBase):
  def __init__(self):
    super(FluoDataFile,self).__init__()

  @staticmethod
  def GetFileType():
    return DataType.FLUO


class excitationBase:
  def __init__(self,initial, final,type=None, T1=None,isUnsafe=False):
    self.initial = initial
    self.final = final
    self.type = type
    self.T1  = T1
    self.isUnsafe = isUnsafe

class excitationValue(excitationBase):
  def __init__(self,initial, final, value, type=None, T1=None,isUnsafe=False,oscilatorForces=None):
    super(excitationValue,self).__init__(initial, final,type=type,T1=T1,isUnsafe=False)
    self.value = value
    self.oscilatorForces = oscilatorForces
