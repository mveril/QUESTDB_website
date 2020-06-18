#!/usr/bin/env python3
import sys
import re
from enum import IntEnum,auto,unique
import numpy as np
from pathlib import Path
from lib import LaTeX
from lib.Format import Format
from TexSoup import TexSoup,TexCmd
from lib.data import dataFileBase,DataType
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file', type=argparse.FileType('r'))
parser.add_argument('--debug', action='store_true', help='Debug mode')
args = parser.parse_args()
lines=args.file.readlines()
soup=TexSoup(lines)
opt=soup.dfbOptions
dfb_Opt= {"defaultType":DataType.ABS,"format":Format.LINE,"suffix":None}
dfbDefaultTypeNode=opt.defaultType
if dfbDefaultTypeNode!=None:
  dfbDefaultType=dfbDefaultTypeNode.expr
  if type(dfbDefaultType) is TexCmd:
    dfb_Opt["defaultType"]=DataType[dfbDefaultType.args[0].value.upper()]

dfbFormatNode=opt.format
if dfbFormatNode!=None:
  dfbFormat=dfbFormatNode.expr
  if type(dfbFormat) is TexCmd:
    dfb_Opt["format"]=Format[dfbFormat.args[0].value.upper()]

dfbSuffixNode=opt.suffix
if dfbSuffixNode!=None:
  dfbSuffix=dfbSuffixNode.expr
  if type(dfbSuffix) is TexCmd:
    dfb_Opt["suffix"]=dfbSuffix.args[0].value
commands=[LaTeX.newCommand(cmd) for cmd in soup.find_all("newcommand")]
dat=LaTeX.tabularToData(soup.tabular,commands)
scriptpath=Path(sys.argv[0]).resolve()
datapath=scriptpath.parents[1]/"static"/"data"
if args.debug:
  datapath=datapath/"test"
if not datapath.exists():
  datapath.mkdir()
datalst=dataFileBase.readFromTable(dat,format=dfb_Opt["format"],default=dfb_Opt["defaultType"],commands=commands)
for data in datalst:
  data.toFile(datapath,dfb_Opt["suffix"])