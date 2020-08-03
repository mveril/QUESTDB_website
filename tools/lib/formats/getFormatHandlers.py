import inspect
from . import formatHandlerBase

def getFormatHandlers(includeUnnamed=False):
  from . import default
  for clsName,Cls in inspect.getmembers(default,inspect.isclass):
    if issubclass(Cls,formatHandlerBase):
      if hasattr(Cls,"__formatName__"):
        yield (Cls.__formatName__,Cls)
      elif(includeUnnamed):
        yield (None,Cls)