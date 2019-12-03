from enum import IntEnum,auto,unique
@unique
class Format(IntEnum):
  LINE=auto()
  COLUMN=auto()
  TBE=auto()