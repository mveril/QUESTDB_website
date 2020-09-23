#!/usr/bin/env python3
import os
import re
import sys
from copy import deepcopy
from statistics import mean
from math import nan,isnan
from pathlib import Path
from collections import defaultdict,OrderedDict
from lib.data import dataFileBase,DataType,method,state,excitationValue
def getValue(ADC2,ADC3,parametername,exADC2=None,exADC3=None):
  def isObject(x):
    return hasattr(x, '__dict__')
  def extractVals(x):
    if isObject(x):
      return vars(x)
    else:
      return x
  def copy(x):
    if isObject(x):
      return deepcopy(x)
    else:
      return x
      
  def isSame(a,b):
    return extractVals(a)==extractVals(b)

  objs=[ADC2,ADC3]
  exs=[exADC2,exADC3]
  if all([x!=None for x in exs]):
    objs=exs
  vals = [getattr(x,parametername) for x in objs]
  if isSame(*vals):
    return copy(vals[0])
  d=OrderedDict()
  for i in range(2):
    key=f"ADC({i+2})"
    d[key]=copy(vals[i])
  index=-1
  while len(vals)<index or index<0:
    if index==0:
      raise ValueError("Operation canceled with ADC {ADC2File.moleucle},{ADC2File.method.basis} with {parametername}")
    print("The Two values are different")
    i=0
    for k in d:
      i+=1
      print(f"{i}){k} value: {extractVals(d[k])}")        
    index=int(input("Select value from the menu:"))
  return vals[index-1]

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', help='Debug mode')
parser.add_argument("--set",nargs="*",type=str)
parser.add_argument("--suffix",type=str)
args=parser.parse_args()
scriptpath=Path(sys.argv[0]).resolve()
datadir=scriptpath.parents[1]/"static"/"data"
sets=None
if args.set is not None:
  setregex = re.compile(r"^(?P<name>[^\[]+)(?:\[(?P<indexes>[\d\-;]+)\])?$")
  sets=dict()
  for myset in args.set:
    m=setregex.match(myset)
    if m:
      name=m.group("name")
      indexes=m.group("indexes")
      if indexes:
        s=set()
        for myindexes in indexes.split(";"):
          ir=myindexes.split("-",2)
          if len(ir)==2:
            for i in range(int(ir[0]),int(ir[1])+1):
              s.add(i)
          else:
            s.add(int(ir[0]))
        sets[name]=s
outputdir=datadir/"test" if args.debug else datadir
ADC23re=re.compile(r"ADC\(([23])\)")  
for t in DataType:
  dFiles=dict()
  for i in range(2,4):
    dFiles[i]=defaultdict(dict)
  currdir=datadir/t.name.lower()
  for file in currdir.glob("*.dat"):
    with file.open('r') as f: # open in readonly mode
      dFile = dataFileBase.readFile(f,t)
      m=ADC23re.match(dFile.method.name)
      if m and (sets == None or dFile.set.name in sets and (len(sets[dFile.set.name])==0 or dFile.set.index in sets[dFile.set.name])):
        dFiles[int(m.group(1))][dFile.molecule][dFile.method.basis]=dFile
  for molecule in dFiles[2]:
    for basis in dFiles[2][molecule]:
      if basis in dFiles[3][molecule]:
        try:
          ADC2File,ADC3File=[dFiles[i][molecule][basis] for i in range(2,4)]
          ADC25File=ADC2File.__class__()
          adc2Dic=vars(ADC2File)
          adc3Dic=vars(ADC3File)
          for k in adc2Dic:
            if k not in ["excitations","method"]:
              val=getValue(ADC2File,ADC3File,k)
              setattr(ADC25File,k,val)
          ADC25File.method=method("ADC(2.5)",ADC2File.method.basis)
          for exADC2 in ADC2File.excitations:
            exADC3s=[x for x in ADC3File.excitations if vars(x.initial) == vars(exADC2.initial) and vars(x.final) == vars(exADC2.final)]
            if len(exADC3s)>0:
              exADC3=exADC3s[0]
              value=mean([(float(x.value)) for x in [exADC2,exADC3]])
              value= "_" if isnan(value)  else "{0:.2f}".format(value) 
              T1 = "_"
              f = "_"
              isUnsafe = exADC2.isUnsafe or exADC3.isUnsafe
              Type=getValue(exADC2,exADC3,"type")
              exADC25=excitationValue(deepcopy(exADC2.initial),deepcopy(exADC2.final),value,Type,T1,isUnsafe,f)
              ADC25File.excitations.append(exADC25)
          ADC25File.toFile(outputdir,args.suffix)

        except ValueError as ex:
           print(ex,file=sys.stderr)