#!/usr/bin/env python3
import sys
import re
from enum import IntEnum,auto,unique
import numpy as np
from pathlib import Path
from lib import LaTeX
from lib.Format import Format
from TexSoup import TexSoup,TexCmd
from lib.data import dataFileBase,DataType,state
from collections import defaultdict
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file', type=argparse.FileType('r'))
parser.add_argument('--debug', action='store_true', help='Debug mode')
args = parser.parse_args()
lines=args.file.readlines()
soup=TexSoup(lines)
opt=soup.dfbOptions
dfb_Opt= {"defaultType":DataType.ABS,"format":Format.LINE,"suffix":None,"initialStates":defaultdict(lambda : state(1,1,"A_1"))}
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
dfbInitialStateNodes=list(opt.find_all("initialState"))
for node in dfbInitialStateNodes:
  initialState=node.expr
  if type(initialState) is TexCmd:
    vRArgs=[arg.value for arg in initialState.args if arg.type=="required"]
    vOArgs=[arg.value for arg in initialState.args if arg.type=="optional"]
    if len(vOArgs)==0:
      defaultstate=state.fromString("1 "+vRArgs[0])
      dfb_Opt["initialStates"].default_factory=lambda : defaultstate
    else:
      mystate=state.fromString("1 "+vRArgs[0])
      dfb_Opt["initialStates"][vOArgs[0]]=mystate
commands=[LaTeX.newCommand(cmd) for cmd in soup.find_all("newcommand")]
dat=LaTeX.tabularToData(soup.tabular,commands)
scriptpath=Path(sys.argv[0]).resolve()
datapath=scriptpath.parents[1]/"static"/"data"
if args.debug:
  datapath=datapath/"test"
if not datapath.exists():
  datapath.mkdir()
datalst=dataFileBase.readFromTable(dat,dfb_Opt["initialStates"],format=dfb_Opt["format"],default=dfb_Opt["defaultType"],commands=commands)
for data in datalst:
  data.toFile(datapath,dfb_Opt["suffix"])