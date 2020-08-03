def formatName(name):
  def formatWrapped(Cls):
    Cls.__formatName__=name
    return Cls
  return formatWrapped