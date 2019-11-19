from enum import IntEnum,auto,unique
@unique
class Orientation(IntEnum):
  LINE=auto()
  COLUMN=auto()