import inspect
from . import default
from . import formatHandlerBase

def getFormatHandlers(includeUnnamed=False):
  for clsName,Cls in inspect.getmembers(default,inspect.isclass):
    if issubclass(Cls,formatHandlerBase):
      if hasattr(Cls,"__formatName__"):
        yield (Cls.__formatName__,Cls)
      elif(includeUnnamed):
        yield (None,Cls)