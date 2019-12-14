from collections import OrderedDict
from TexSoup import TexSoup
from .LaTeX import newCommand
from enum import IntEnum,auto,unique,IntFlag
from .Format import Format
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
  def convertState(StateTablelist,default=dataType.ABS,firstState=state(1,1,"A_1"),commands=[]):
    tmplst=[]
    for TexState in StateTablelist:
      math=TexState.find("$")
      lst=list(math.contents)
      mathsoup=TexSoup(str(lst[0]))
      newCommand.runAll(mathsoup,commands)
      st=str(mathsoup)
      m=re.match(r"^\^(?P<multiplicity>\d)(?P<symm>[^\s\[(]*)\s*(?:\[(?:\\mathrm{)?(?P<special>\w)(?:})\])?\s*\((?P<type>[^\)]*)\)",st)
      seq=m.group("multiplicity","symm")
      spgrp=m.group("special")
      if spgrp is not None and spgrp=="F":
        trsp=dataType.FLUO
      else:
        trsp=default
      tygrp=m.group("type")
      tmplst.append((*seq,trsp,tygrp))
    lst=[]
    for index,item in enumerate(tmplst):
      unformfirststate=(str(firstState.multiplicity),firstState.symetry)
      count=([unformfirststate]+tmplst[:index+1]).count(item)
      lst.append((state(count,int(item[0]),item[1]),item[2],item[3]))
    return lst

  @staticmethod
  def readFromTable(table,format=Format.LINE,default=dataType.ABS ,firstState=state(1,1,"A_1"),commands=[]):
    datalist=list()
    switcher={
      dataType.ABS:AbsDataFile,
      dataType.FLUO:FluoDataFile,
      dataType.ZPE:ZPEDataFile
    }
    if format==Format.LINE:
      for col in range(1,np.size(table,1)):
        col=table[:,col]
        mymolecule=str(col[0])
        mymethod=method(str(col[2]),str(col[1]))
        finsts=dataFileBase.convertState(table[3:,0],firstState,commands=commands)
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
            data.excitations.append(excitationValue(firstState,finst[0],val,type=finst[2]))
        for datamtbe in datacls.values():
          datalist.append(datamtbe)
      return datalist
    elif format==Format.COLUMN:
      subtablesindex=list()
      firstindex=2
      for i in range(3,np.size(table,0)):
        if str(table[i,0])!="":
          subtablesindex.append((firstindex,i-1))
          firstindex=i
      for first, last in subtablesindex:
        for col in range(2,np.size(table,1)):
          datacls=dict()
          col=table[:,col]
          mymolecule=str(table[first,0])
          mymethod=method(str(col[1]),str(col[0]))
          finsts=dataFileBase.convertState(table[first:last+1,1],default=default,firstState=firstState,commands=commands)
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
              data.excitations.append(excitationValue(firstState,finst[0],val,type=finst[2]))
          for value in datacls.values():
            datalist.append(value)
      return datalist
    elif format==Format.TBE:
      subtablesindex=list()
      firstindex=2
      for i in range(3,np.size(table,0)):
        if str(table[i,0])!="":
          subtablesindex.append((firstindex,i-1))
          firstindex=i
      for first, last in subtablesindex:
        datacls=dict()
        mymolecule=str(table[first,0])
        mymethod=(method("TBE"),method("TBE-corr"))
        finsts=dataFileBase.convertState(table[first:last+1,1],default=default,firstState=firstState,commands=commands)
        for index,row in enumerate(table[first:last+1,]):
          def toFloat(x):
            try:
              return float(x)
            except ValueError:
              return None
          oscilatorForces=toFloat(str(row[2]))
          T1 = toFloat(str(row[3]))
          val = toFloat(str(row[4]))
          corr = toFloat(str(row[7]))
          finst=finsts[index]
          dt=finst[1]
          if dt in datacls:
            datamtbe = datacls[dt]
          else:
            cl=switcher[dt]
            datamtbe=[]
            for met in mymethod:
              data=cl()
              data.molecule=mymolecule
              data.method=met
              datamtbe.append(data)
            datacls[dt]=datamtbe
            vs=[val,corr]
          for i in range(2):
            datamtbe[i].excitations.append(excitationValue(firstState,finst[0],vs[i],type=finst[2],T1=T1,forces=oscilatorForces))
        for value in datacls.values():
          for dat in value:
            datalist.append(dat)
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
    fileName="{}_{}.dat".format(self.molecule.lower().replace(" ","_"),self.method.name) if self.method.basis==None else "{}_{}_{}.dat".format(self.molecule.lower().replace(" ","_"),self.method.name,self.method.basis)
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
          mystr="  {:8s}{:7s}{:10s}{:8s}{:6s}{:13s}{:40s}{:10s}{:15s}{}\n".format(
            str(ex.initial.number),
            str(ex.initial.multiplicity),
            ex.initial.symetry,
            str(ex.final.number),
            str(ex.final.multiplicity),
            ex.final.symetry,"{"+str(ex.type)+"}" if ex.type is not None else "_",
            str(ex.value) if ex.value is not None else "_",
            str(ex.T1) if ex.T1 is not None else "_",
            str(ex.oscilatorForces) if ex.oscilatorForces is not None else "_",
            str(ex.isUnsafe).lower())
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
  def __init__(self,initial, final, **kwargs):
    self.initial = initial
    self.final = final
    self.type = kwargs["type"] if "type" in kwargs else None
    self.T1 = kwargs["T1"] if "T1" in kwargs else None
    self.isUnsafe = kwargs["unsafe"] if "unsafe" in kwargs else False

class excitationValue(excitationBase):
  def __init__(self,initial, final, value,**kwarg):
    supkwarg=kwarg.copy()
    for item in ["forces","corrected"]:
      if item in supkwarg:
        supkwarg.pop(item)
    super(excitationValue,self).__init__(initial, final,**supkwarg)
    self.value = value
    self.oscilatorForces=kwarg["forces"] if "forces" in kwarg else None
