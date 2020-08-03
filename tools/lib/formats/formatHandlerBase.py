from abc import ABCMeta
from abc import abstractmethod
class formatHandlerBase(object):
  __metaclass__ = ABCMeta
  def __init__(self,TexOps, commands=[]):
    self.TexOps=TexOps
    self.commands=commands
  @abstractmethod
  def readFromTable(self,table):
    raise NotImplementedError()