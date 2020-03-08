#!/usr/bin/env python3
import sys
import re
from enum import IntEnum,auto,unique
import numpy as np
from pathlib import Path
from lib import LaTeX
from lib.Format import Format
from TexSoup import TexSoup
from lib.data import dataFileBase,dataType
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file', type=argparse.FileType('r'))
parser.add_argument('--defaultType', type=str, choices=[t.name for t in list(dataType)])
parser.add_argument('--format',type=str, choices=[t.name for t in list(Format)],default=Format.LINE.name)
parser.add_argument('--debug', action='store_true', help='Debug mode'
)
args = parser.parse_args()
print(args)
lines=args.file.readlines()
soup=TexSoup(lines)
commands=[LaTeX.newCommand(cmd) for cmd in soup.find_all("newcommand")]
dat=LaTeX.tabularToData(soup.tabular,commands)
scriptpath=Path(sys.argv[0]).resolve()
datapath=scriptpath.parents[1]/"static"/"data"
if args.debug:
  datapath=datapath/"test"
if not datapath.exists():
  datapath.mkdir()
datalst=dataFileBase.readFromTable(dat,format=Format[args.format],default=dataType[args.defaultType],commands=commands)
for data in datalst:
  data.toFile(datapath)