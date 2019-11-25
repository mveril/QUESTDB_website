from collections import OrderedDict
from enum import IntEnum,auto,unique,IntFlag
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

  @property
  def IsTBE(self):
    return self.method.name=="TBE"

  @staticmethod
  def GetFileType():
    pass

  @staticmethod
  def convertState(StateTablelist,default=dataType.ABS,firstState=state(1,1,"A_1")):
    tmplst=[]
    for TexState in StateTablelist:
      trtype=default
      lst=list(TexState.find("$").contents)
      st=str(lst[0])
      m=re.match(r"^\^(?P<multiplicity>\d)(?P<symm>[^\s\[(]*)\s*(?:\[(?:\\mathrm{)?(?P<special>\w)(?:})\])?\s*\((?P<type>[^\)]*)\)",st)
      seq=m.group("multiplicity","symm")
      spgrp=m.group("special")
      if spgrp is not None and spgrp=="F":
        trtype=dataType.FLUO
      tmplst.append((*seq,trtype))
    lst=[]
    for index,item in enumerate(tmplst):
      unformfirststate=(str(firstState.multiplicity),firstState.symetry)
      count=([unformfirststate]+tmplst[:index+1]).count(item)
      lst.append((state(count,int(item[0]),item[1]),item[2]))
    return lst

  @staticmethod
  def readFromTable(table,orientation=Orientation.LINE,default=dataType.ABS ,firstState=state(1,1,"A_1")):
    datalist=list()
    switcher={
      dataType.ABS:AbsDataFile,
      dataType.FLUO:FluoDataFile,
      dataType.ZPE:ZPEDataFile
    }
    if orientation==Orientation.LINE:
      for col in range(1,np.size(table,1)):
        col=table[:,col]
        mymolecule=str(col[0])
        mymethod=method(str(col[2]),str(col[1]))
        finsts=dataFileBase.convertState(table[3:,0],firstState)
        datacls=dict()
        for index,cell in enumerate(col[3:]):
          if str(cell)!="":
            val= list(cell.contents)[0]
            val=float(str(val))
            finst=finsts[index]
            dt=finst[1]
            if dt in datacls:
              data=datacls[dt]
            else:
              cl=switcher[dt]
              data=cl()
              data.molecule=mymolecule
              data.method=mymethod
            data.excitations.append(excitationValue(firstState,finst[0],val))
        for value in datacls.values():
          datalist.append(value)
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
          col=table[:,col]
          mymolecule=str(table[first,0])
          mymethod=method(str(col[1]),str(col[0]))
          finsts=dataFileBase.convertState(table[first:last+1,1],default=default,firstState=firstState)
        for col in range(2,np.size(table,1)):
          datacls=dict()
          col=table[:,col]
          mymolecule=str(table[first,0])
          mymethod=method(str(col[1]),str(col[0]))
          finsts=dataFileBase.convertState(table[first:last+1,1],default=default,firstState=firstState)
          for index,cell in enumerate(col[first:last+1]):
            if str(cell)!="":
              val= list(cell.contents)[0]
              val=float(str(val))
              finst=finsts[index]
              dt=finst[1]
              if dt in datacls:
                data=datacls[dt]
              else:
                cl=switcher[dt]
                data=cl()
                data.molecule=mymolecule
                data.method=mymethod
                datacls[dt]=data
              data.excitations.append(excitationValue(firstState,finst[0],val))
          for value in datacls.values():
            datalist.append(value)
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
#######################  #######################   #################
# Number  Spin  Symm       Number  Spin  Symm         E_{:5s} Corr\n""".format(self.GetFileType().name.lower()))
        for ex in self.excitations:
          mystr="  {:8s}{:7s}{:10s}{:8s}{:6s}{:13s}{:8s}{}\n".format(str(ex.initial.number),str(ex.initial.multiplicity),ex.initial.symetry,str(ex.final.number),str(ex.final.multiplicity),ex.final.symetry,str(ex.value) if ex.value is not None else "_",str(ex.Correction) if ex.Correction is not None else "_")
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
  def __init__(self,initial, final, value,*args):
    super(excitationValue,self).__init__(initial, final)
    self.value = value
    self.Correction=args[0] if len(args)>0 else None