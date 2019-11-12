#!/usr/bin/env python3
import sys
import re
import numpy as np
from pathlib import Path
from lib import LaTeX
from TexSoup import TexSoup
from lib.data import AbsDataFile,ZPEDataFile,FluoDataFile,dataType
import argparse
DEBUG=False
parser = argparse.ArgumentParser()
parser.add_argument('--file', type=argparse.FileType('r'))
parser.add_argument('--type', type=str, choices=[t.name for t in list(dataType)])
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
for col in range(3,np.size(dat,1)):
  filecls.readFromTable(dat,col).toFile(datapath)