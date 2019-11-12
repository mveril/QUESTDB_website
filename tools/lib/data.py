from collections import OrderedDict
from enum import IntEnum,auto,unique
import re

class state:
  def __init__(self,number, multiplicity, symetry):
    self.number = number
    self.multiplicity = multiplicity
    self.symetry = symetry


@unique
class dataType(IntEnum):
  ABS=auto()
  FLUO=auto()
  ZPE=auto()
class dataFileBase(object):
  def __init__(self):
    self.molecule = ''
    self.comment = ''
    self.code = None
    self.method = None
    self.excitations = []
    self.DOI = ''

  @staticmethod
  def GetFileType():
    pass

  @staticmethod
  def convertState(StateTablelist,firstState=state(1,1,"A_1")):
    tmplst=[]
    for TexState in StateTablelist:
      st=list(TexState.find("$").contents)[0]
      m=re.match(r"^\^(?P<multiplicity>\d)(?P<GPS>\S+)",st)
      seq=m.groups()
      tmplst.append(seq)
    lst=[]
    for index,item in enumerate(tmplst):
      unformfirststate=(str(firstState.multiplicity),firstState.symetry)
      count=([unformfirststate]+tmplst[:index+1]).count(item)
      lst.append(state(count,int(item[0]),item[1]))
    return lst

  @classmethod
  def readFromTable(cls, table,column,firstState=state(1,1,"A_1")):
    data=cls()
    col=table[:,column]
    data.molecule=str(col[0])
    data.method=method(str(col[2]),str(col[1]))
    finsts=cls.convertState(table[3:,0],firstState)
    for index,cell in enumerate(col[3:]):
      if str(cell)!="":
        val= list(cell.contents)[0]
        val=float(str(val))
        data.excitations.append(excitationValue(firstState,finsts[index],val))
    return data
  
  def getMetadata(self):
    dic=OrderedDict()
    dic["Molecule"]=self.molecule
    dic["Comment"]=self.comment
    dic["code"]="" if self.code is None else self.code.toDataString()
    dic["method"]="" if self.method is None else self.method.toDataString()
    dic["DOI"]="" if self.DOI is None else self.DOI
    return dic
  
  def toFile(self,datadir):
    subpath=datadir/self.GetFileType().name.lower()
    if not subpath.exists():
      subpath.mkdir()
    file=subpath/"{}_{}_{}.dat".format(self.molecule.lower().replace(" ","_"),self.method.name,self.method.basis)
    if not file.exists():
      with file.open("w") as f:
        for key,value in self.getMetadata().items():
          if value is not None:
            f.write("# {:9s}: {}\n".format(key,value))
        f.write("""
# Initial state            Final state               Energies (eV)
#######################  #######################   ###############
# Spin  Number  Symm       Spin  Number  Symm         E_{}\n""".format(self.GetFileType().name.lower()))
        for ex in self.excitations:
          mystr="  {:6s}{:9s}{:10s}{:6s}{:8s}{:13s}{}\n".format(str(ex.initial.number),str(ex.initial.multiplicity),ex.initial.symetry,str(ex.final.number),str(ex.final.multiplicity),ex.final.symetry,str(ex.value))
          f.write(mystr)
class method:
  def __init__(self,name, basis):
    self.name = name
    self.basis = basis

  @staticmethod
  def fromString(string):
    vals = string.split(",")
    if (vals.length == 2):
      return method(vals[0], vals[1])
    else:
      return method(vals[0], None)

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

  @classmethod
  def readFromTable(cls, table,column,firstState=state(1,1,"A_1")):
    data=super().readFromTable(table,column,firstState=firstState)
    return data
class AbsDataFile(oneStateDataFileBase):
  def __init__(self):
    super(AbsDataFile,self).__init__()
  
  @staticmethod
  def GetFileType():
    return dataType.ABS

class FluoDataFile(oneStateDataFileBase):
  def __init__(self):
    super(FluoDataFile,self).__init__()

  @staticmethod
  def GetFileType():
    return dataType.FLUO

class twoStateDataFileBase(dataFileBase):
  def __init__(self):
    super(twoStateDataFileBase,self).__init__()
    self.GS=None
    self.ES=None

  @classmethod
  def readFromTable(cls, table,column,firstState=state(1,1,"A_1")):
    data=super().readFromTable(table,column,firstState=firstState)
    return data
  def getMetadata(self):
    dic=super(twoStateDataFileBase,self).getMetadata()
    dic["GS"]= "" if self.GS is None else self.GS.toDataString()
    dic["ES"]="" if self.ES is None else self.ES.toDataString()
    dic.move_to_end("DOI")
    return dic

class ZPEDataFile(twoStateDataFileBase):
  def __init__(self):
    super(ZPEDataFile,self).__init__()
  
  @staticmethod
  def GetFileType():
    return dataType.ZPE

class excitationBase:
  def __init__(self,initial, final):
    self.initial = initial
    self.final = final

class excitationValue(excitationBase):
  def __init__(self,initial, final, value):
    super(excitationValue,self).__init__(initial, final)
    self.value = value