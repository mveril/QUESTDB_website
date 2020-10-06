from abc import ABCMeta, abstractmethod
class formatHandlerBase(object, metaclass=ABCMeta):
  def __init__(self,TexOps, commands=[]):
    self.TexOps=TexOps
    self.commands=commands
  @abstractmethod
  def readFromTable(self,table):
    raise NotImplementedError()