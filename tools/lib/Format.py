from enum import IntEnum,auto,unique
@unique
class Format(IntEnum):
  LINE=auto()
  COLUMN=auto()
  DOUBLECOLUMN=auto()
  TBE=auto()
  DOUBLETBE=auto()