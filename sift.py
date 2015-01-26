#!/usr/bin/python2.7
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  orf_reader.py
#
# Copyright 2014 CoBiG^2 <f.pinamartins@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  orf_reader.py v1.0
#  Author: Bruno Costa
#  Last update: 03/10/2014

import argparse
import string
import re


parser = argparse.ArgumentParser(description="Remote tool to getting zones or links or something for rad sequence data Creates a map or something")
parser.add_argument("-i",dest="dir",required=False, help="pecified directory for tags.tsv files, if no file directory is provided uses current dir.")
#arg = parser.parse_args()

import string
import re
import glob
import string


fileIn="/Users/bcosta/Dropbox/Tese/Tese Tymus/Results/Dados/Results/sift-IFNG.txt"
#fileIn=arg.dir
fileOut=None

dataIn=open(fileIn, "r")
#dataOut=open(fileOut, "w")
dataIn=dataIn.read().split("\n")
del dataIn[0]
res={}

def avg(arry):
    #calula media
    sum=0
    for i in arry:
        sum+=i
    return sum/len(arry)


for i in dataIn:
    tmp=i.split("\t")
    try:
        if tmp[2]=='157':
            print tmp
        tmpB=res[tmp[2]]
        tmpB.append(float(tmp[6]))
        res[tmp[2]]=tmpB
    except:
        res[tmp[2]]=[float(tmp[6])]


for i in res:
    print "%s %s" %(i,avg(res[i]))


