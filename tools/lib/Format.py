from enum import IntEnum,auto,unique
@unique
class Format(IntEnum):
  LINE=auto()
  COLUMN=auto()
  DOUBLECOLUMN=auto()
  EXOTICCOLUMN=auto()
  TBE=auto()
  DOUBLETBE=auto()