from collections import OrderedDict
from TexSoup import TexSoup
from .LaTeX import newCommand
from .utils import getValFromCell,checkFloat
from TexSoup import TexNode,TexEnv
from enum import IntEnum,auto,unique,IntFlag
from .Format import Format
import re
import numpy as np
import json

class state:
  def __init__(self,number, multiplicity, symetry):
    self.number = number
    self.multiplicity = multiplicity
    self.symetry = symetry


@unique
class dataType(IntEnum):
  ABS=auto()
  FLUO=auto()
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
        trsp=dataType.FLUO
      else:
        trsp=default
      tygrp=m.group("type")
      tmplst.append((mul,symm,trsp,tygrp))
    lst=[]
    for index,item in enumerate(tmplst):
      unformfirststate=(firstState.multiplicity,firstState.symetry)
      countlst=[unformfirststate]+[(it[0],it[1]) for it in tmplst[:index+1]]
      countitem=(item[0],item[1])
      count=countlst.count(countitem)
      lst.append((state(count,item[0],item[1]),item[2],item[3]))
    return lst

  @staticmethod
  def readFromTable(table,format=Format.LINE,default=dataType.ABS ,firstState=state(1,1,"A_1"),commands=[]):
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

    datalist=list()
    switcher={
      dataType.ABS:AbsDataFile,
      dataType.FLUO:FluoDataFile,
    }
    if format==Format.LINE:
      for col in range(1,np.size(table,1)):
        col=table[:,col]
        mymolecule=str(col[0])
        mymethod=method(str(col[2]),str(col[1]))
        finsts=dataFileBase.convertState(table[3:,0],default=default,firstState=firstState,commands=commands)
        datacls=dict()
        for index,cell in enumerate(col[3:]):
          if str(cell)!="":
            val,unsafe=getValFromCell(cell)
            finst=finsts[index]
            dt=finst[1]
            if dt in datacls:
              data=datacls[dt]
            else:
              cl=switcher[dt]
              data=cl()
              datacls[dt]=data
              data.molecule=mymolecule
              data.method=mymethod
            data.excitations.append(excitationValue(firstState,finst[0],val,type=finst[2],isUnsafe=unsafe))
        for value in datacls.values():
          datalist.append(value)
      return datalist
    elif format==Format.COLUMN:
      subtablesindex=getSubtableIndex(table)
      for first, last in subtablesindex:
        for col in range(2,np.size(table,1)):
          datacls=dict()
          col=table[:,col]
          mymolecule=str(table[first,0])
          mymethod=method(str(col[1]),str(col[0]))
          finsts=dataFileBase.convertState(table[first:last+1,1],default=default,firstState=firstState,commands=commands)
          for index,cell in enumerate(col[first:last+1]):
            if str(cell)!="":
              val,unsafe=getValFromCell(cell)
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
    elif format==Format.DOUBLECOLUMN:
      datacls=dict()
      subtablesMol=getSubtableIndex(table)
      for firstMol, lastMol in subtablesMol:
        mymolecule=str(table[firstMol,0])
        moltable=table[firstMol:lastMol+1,:]
        subtablestrans=getSubtableIndex(moltable,firstindex=0,column=1,count=2)
        for firstTrans,lastTrans in subtablestrans:
          mytrans=moltable[firstTrans:lastTrans+1,:]
          mytransdesc=mytrans[0:2,1]
          for i in range(2):      
            try:
              mathsoup=TexSoup(mytransdesc[i])
            except:
              print(f"Error when parsing latex state: {str(mytransdesc[i])}")
              exit(-1)
            newCommand.runAll(mathsoup,commands)
            mytransdesc[i]=str(mathsoup)
          for colindex in range(3,np.size(table,1)):
            col=mytrans[:,colindex]
            mybasis=str(table[1,colindex])
            for index,cell in enumerate(col):
              methodnameAT1=str(mytrans[index,2])
              PTString=r"($\%T_1$)"
              HasT1=methodnameAT1.endswith(PTString)
              if HasT1:
                methodname=methodnameAT1[:-len(PTString)]
              else:
                methodname=str(methodnameAT1)
              mymethod=method(methodname,mybasis)
              strcell=str(cell)
              if strcell!="":
                if HasT1:
                  m=re.match(r"^(?P<value>[-+]?\d+\.?\d*)\s*(?:\((?P<T1>\d+\.?\d*)\\\%\))?",strcell)
                  val,unsafe=getValFromCell(TexSoup(m.group("value")))
                  T1=m.group("T1")
                else:
                  m=re.match(r"^[-+]?\d+\.?\d*",strcell)
                  val,unsafe=getValFromCell(TexSoup(m.group(0)))
                  T1=None
                if (mymolecule,mymethod.name,mymethod.basis) in datacls:
                  data=datacls[(mymolecule,mymethod.name,mymethod.basis)]
                else:
                  data=AbsDataFile()
                  data.molecule=mymolecule
                  data.method=mymethod
                  datacls[(mymolecule,mymethod.name,mymethod.basis)]=data
                infin=mytransdesc[0].split(r"\rightarrow")
                for i,item in enumerate(infin):
                  m=re.match(r"^(?P<number>\d)\\[,:;\s]\s*\^(?P<multiplicity>\d)(?P<sym>\S*)",item.strip())
                  infin[i]=state(m.group("number"),m.group("multiplicity"),m.group("sym"))
                data.excitations.append(excitationValue(infin[0],infin[1],val,type=mytransdesc[1],isUnsafe=unsafe,T1=T1))
        for value in datacls.values():
          datalist.append(value)
      return datalist
    elif format==Format.EXOTICCOLUMN:
      import json
      subtablesindex=getSubtableIndex(table)
      for first, last in subtablesindex:
        valDic=dict()
        mymolecule=str(table[first,0])
        for col in range(2,np.size(table,1)):
          col=table[:,col]
          basis=str(col[0])
          mymethcell=list(col[1])
          if isinstance(mymethcell[0],TexNode) and mymethcell[0].name=="$":
            kindSoup=TexSoup("".join(list(mymethcell[0].expr.all)))
            newCommand.runAll(kindSoup,commands)
            kind=str(kindSoup)
            methodnameSoup=TexSoup(mymethcell[1].value)
            newCommand.runAll(methodnameSoup,commands)
            methodname=str(methodnameSoup)
          else:
            kind=""
            methtex=col[1]
            newCommand.runAll(methtex,commands)
            methodname=str(methtex)
          mymethod=method(methodname,basis)
          methkey=json.dumps(mymethod.__dict__)
          finsts=dataFileBase.convertState(table[first:last+1,1],default=default,firstState=firstState,commands=commands)
          for index,cell in enumerate(col[first:last+1]):
            if str(cell)!="":
              val,unsafe=getValFromCell(cell)
              finst=finsts[index]
              dt=finst[1]
              if dt in valDic:
                dtDic=valDic[dt]
              else:
                dtDic=dict()
                valDic[dt]=dtDic
              if not methkey in dtDic:
                dtDic[methkey]=dict()
              dataDic=dtDic[methkey]
              exkey=(json.dumps(finst[0].__dict__,),finst[2])
              if not exkey in dataDic:
                dataDic[exkey]=dict()
              if kind=='':
                dataDic[exkey][kind]=(val,unsafe)
              else:
                dataDic[exkey][kind]=val
              #data.excitations.append(excitationValue(firstState,finst[0],val,type=finst[2]))
        for dt,methdic in valDic.items():
          for methstring,exdic in methdic.items():
            data=switcher[dt]()
            data.molecule=mymolecule
            methdic=json.loads(methstring)
            data.method=method(methdic["name"],methdic["basis"])
            for exstr,values in exdic.items():
              stDict=json.loads(exstr[0])
              ty=exstr[1]
              st=state(stDict["number"],stDict["multiplicity"],stDict["symetry"])
              T1=values["\\%T_1"] if "\\%T_1" in values  else None
              oF= values["f"] if "f" in values  else None
              val,unsafe=values[""]
              data.excitations.append(excitationValue(firstState,st,val,type=ty,T1=T1,isUnsafe=unsafe,oscilatorForces=oF))
              datalist.append(data)
      return datalist
    elif format==Format.TBE:
      subtablesindex=getSubtableIndex(table)
      for first, last in subtablesindex:
        datacls=dict()
        mymolecule=str(table[first,0])
        mymethod=(method("TBE(FC)"),method("TBE"))
        finsts=dataFileBase.convertState(table[first:last+1,1],default=default,firstState=firstState,commands=commands)
        for index,row in enumerate(table[first:last+1,]):
          oscilatorForces=checkFloat(str(row[2]))
          T1 = checkFloat(str(row[3]))
          val,unsafe = getValFromCell(row[4])
          corr,unsafecorr = getValFromCell(row[7])
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
          uns=[unsafe,unsafecorr]
          for i in range(2):
            datamtbe[i].excitations.append(excitationValue(firstState,finst[0],vs[i],type=finst[2],T1=T1,oscilatorForces=oscilatorForces,isUnsafe=uns[i]))
        for value in datacls.values():
          for dat in value:
            datalist.append(dat)
      return datalist
    elif format==Format.DOUBLETBE:
      datacls=dict()
      subtablesMol=getSubtableIndex(table)
      for firstMol, lastMol in subtablesMol:
        data=AbsDataFile()
        data.molecule=str(table[firstMol,0])
        data.method=method("TBE","CBS")
        for mytrans in table[firstMol:lastMol+1]:
          try:
            mathsoup=TexSoup(mytrans[1])
          except:
            print(f"Error when parsing latex state: {str(mytransdesc[i])}")
            exit(-1)
          newCommand.runAll(mathsoup,commands)
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
    return dataType.ABS

class FluoDataFile(oneStateDataFileBase):
  def __init__(self):
    super(FluoDataFile,self).__init__()

  @staticmethod
  def GetFileType():
    return dataType.FLUO


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
