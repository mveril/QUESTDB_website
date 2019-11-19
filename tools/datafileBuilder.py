#!/usr/bin/env python3
import sys
import re
from enum import IntEnum,auto,unique
import numpy as np
from pathlib import Path
from lib import LaTeX
from lib.Orientation import Orientation
from TexSoup import TexSoup
from lib.data import AbsDataFile,ZPEDataFile,FluoDataFile,dataType
import argparse
DEBUG=True
parser = argparse.ArgumentParser()
parser.add_argument('--file', type=argparse.FileType('r'))
parser.add_argument('--type', type=str, choices=[t.name for t in list(dataType)])
parser.add_argument('--MoleculeOrentation',type=str, choices=[t.name for t in list(Orientation)],default=Orientation.LINE.name)
args = parser.parse_args()
print(args)
lines=args.file.readlines()
soup=TexSoup(lines)
commands=[LaTeX.newCommand(cmd) for cmd in soup.find_all("newcommand")]
dat=LaTeX.tabularToData(soup.tabular,commands)
scriptpath=Path(sys.argv[0]).resolve()
datapath=scriptpath.parents[1]/"static"/"data"
if DEBUG:
  datapath=datapath/"test"
if not datapath.exists():
  datapath.mkdir()
switcher={
  dataType.ABS: AbsDataFile,
  dataType.FLUO: FluoDataFile,
  dataType.ZPE: ZPEDataFile
}
filecls=switcher.get(dataType[args.type])
datalst=filecls.readFromTable(dat,Orientation[args.MoleculeOrentation])
for data in datalst:
  data.toFile(datapath)