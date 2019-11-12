import re
from TexSoup import TexSoup,TexCmd,TexNode
from .utils import *
import itertools
from enum import Enum
from abc import ABCMeta
class commandBase(metaclass=ABCMeta):
  def __init__(self,source,supportedTexType):
    if not (source.name==supportedTexType):
      raise ValueError(source+" is not a "+supportedTexType)
    self.source=source
  
  def __str__(self):
    return self.source.__str__

  def __repr__(self):
    return self.source.__repr__()

class newCommand(commandBase):
  def __init__(self,source):
    super(newCommand, self).__init__(source,"newcommand")
    
  @property
  def commandName(self):
    return self.source.args[0].value[1:]

  @property
  def argNum(self):
    return 0 if self.source.args[1].type!='optional' else self.source.args[1].value

  @property
  def result(self):
    return nodify(list(self.source.args[len(self.source.args)-1].contents))

  def exist(self,tex):
    exist=tex.find(self.commandName)!=None
    return exist

  def run(self,tex):
    cmds=list(tex.find_all(self.commandName))
    if len(cmds)==0:
      raise ValueError("Command not found in tex")
    else:  
      for cmd in cmds:
        if self.argNum==0:
          res=self.result
        else:
          resultstr=str(self.result)
          res=TexSoup(re.sub('\#([1-{}])'.format(self.argNum),lambda m: cmd.args[int(m.group(1))-1].value,resultstr))
        soup=TexSoup(res)
        tex.replace(cmd,soup)
    
    def tryrun():
      cmds=list(tex.find_all(self.commandName))
      if len(cmds)!=0:
        for cmd in cmds:
          if self.argNum==0:
            res=self.result
          else:
            res=re.sub('#[1-{}]'.format(self.argNum),lambda m: cmd.args[int(m.group(1))-1],self.result)
          soup=TexSoup(res)
          tex.replace(cmd,soup)

  @staticmethod
  def runAll(tex,collection):
    cmds=[cmd for cmd in collection if cmd.exist(tex)]
    if(len(cmds)>0):
      for cmd in cmds:
        cmd.run(tex)
      newCommand.runAll(tex,collection)
class columnAlignment(Enum):
  Left = "l"
  Right = "r"
  Center = "c"
class multiColumn(commandBase):
  def __init__(self,source):
    super(multiColumn,self).__init__(source,"multicolumn")

  @property
  def cols(self):
    return int(self.source.args[0].value)

  @property
  def align(self):
    return columnAlignment(self.source.args[1].value)

  @property
  def contents(self):
    return nodify(list(self.source.args[2].contents))
def tabularToData(table,commands=None):
  if table.name=="tabular":
    ctable=str(table)
    ctable=ctable.split("\n")
    ctable=ctable[1:len(ctable)-1]
    rows=[x.strip() for x in ''.join(ctable).split(r'\\') if x.strip()!='']  
    ltable=[]
    ltable=[[c.strip() for c in r.split("&")] for r in rows]
    lnewtable=[]
    for row in ltable:
      r=[]
      for item in row:
        texitem=TexSoup(item)
        child=list(texitem.children)
        if(len(child)==1 and child[0].name=="multicolumn"):
          mcolel=child[0]
          mcol=multiColumn(mcolel)
          el=mcol.contents
          if commands!=None:
            newCommand.runAll(el,commands)
          for i in range(int(mcol.cols)):
            r.append(el)
        else:
          if type(item) is str:
            el=TexSoup(item)
          else:
            el=item
          el=desarg(el)
          if commands!=None:
            newCommand.runAll(el,commands)
          r.append(el)
      lnewtable.append(r)
    lens=[len(x) for x in lnewtable]
    #Check if all rows have the same dimension
    if(len(set(lens))!=1):
      raise ValueError("This tabular is not supported")
    import numpy as np
    table=np.array(lnewtable,TexNode)
    return table
  else:
    raise ValueError("Only tabular LaTeX environment is supported")