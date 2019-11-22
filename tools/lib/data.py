from collections import OrderedDict
from enum import IntEnum,auto,unique
from .Orientation import Orientation
import re
import numpy as np

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
      lst=list(TexState.find("$").contents)
      st=str(lst[0])
      m=re.match(r"^\^(?P<multiplicity>\d)(?P<symm>[^\s\[(]*)\s*(?:\[(?:\\mathrm{)?(?P<special>\w)(?:})\])?\s*\((?P<type>[^\)]*)\)",st)
      seq=m.group("multiplicity","symm")
      tmplst.append(seq)
    lst=[]
    for index,item in enumerate(tmplst):
      unformfirststate=(str(firstState.multiplicity),firstState.symetry)
      count=([unformfirststate]+tmplst[:index+1]).count(item)
      lst.append(state(count,int(item[0]),item[1]))
    return lst

  @classmethod
  def readFromTable(cls, table,orientation=Orientation.LINE ,firstState=state(1,1,"A_1")):
    datalist=list()
    if orientation==Orientation.LINE:
      for col in range(1,np.size(table,1)):
        data=cls()
        col=table[:,col]
        data.molecule=str(col[0])
        data.method=method(str(col[2]),str(col[1]))
        finsts=cls.convertState(table[3:,0],firstState)
        for index,cell in enumerate(col[3:]):
          if str(cell)!="":
            val= list(cell.contents)[0]
            val=float(str(val))
            data.excitations.append(excitationValue(firstState,finsts[index],val))
        datalist.append(data)
      return datalist
    else:
      subtablesindex=list()
      firstindex=2
      for i in range(3,np.size(table,0)):
        if str(table[i,0])!="":
          subtablesindex.append((firstindex,i-1))
          firstindex=i
      for first, last in subtablesindex:
        for col in range(2,np.size(table,1)):
          data=cls()
          col=table[:,col]
          data.molecule=str(table[first,0])
          data.method=method(str(col[1]),str(col[0]))
          finsts=cls.convertState(table[first:last+1,1],firstState)
          for index,cell in enumerate(col[first:last+1]):
            if str(cell)!="":
              val= list(cell.contents)[0]
              val=float(str(val))
              data.excitations.append(excitationValue(firstState,finsts[index],val))
          datalist.append(data)
      return datalist
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
# Number  Spin  Symm       Number  Spin  Symm         E_{}\n""".format(self.GetFileType().name.lower()))
        for ex in self.excitations:
          mystr="  {:8s}{:7s}{:10s}{:8s}{:6s}{:13s}{}\n".format(str(ex.initial.number),str(ex.initial.multiplicity),ex.initial.symetry,str(ex.final.number),str(ex.final.multiplicity),ex.final.symetry,str(ex.value))
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
  def readFromTable(cls, table,orientation=Orientation.LINE,firstState=state(1,1,"A_1")):
    data=super().readFromTable(table,orientation,firstState=firstState)
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
  def readFromTable(cls, table,orientation=Orientation.LINE,firstState=state(1,1,"A_1")):
    data=super().readFromTable(table,Orientation,firstState=firstState)
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