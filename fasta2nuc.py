#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  fasta2nuc.py
#  
#  Copyright 2013 Bruno Costa <brunovasquescosta@gmail.com>
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
#  fasta2nuc.py v1.0
#  Author: Bruno Costa
#  Last update: 21/01/2014

import argparse
import string

parser = argparse.ArgumentParser(description="Remote tool to convert fasta to phy for paml")

parser.add_argument("-i",dest="i", required=True, help="Provide the input file")
parser.add_argument("-o",dest="o", help="Output path")
parser.add_argument("-s",dest="stop",default=False, help="weather or not to remove stop codons")#not used

arg = parser.parse_args()

#gene="hoxb4"
stop=["TAA","TAG","TGA"]
countRm=0

#pathIn="../MAFFT/"+gene+"/"+gene+".fasta"
#pathOut="../MAFFT/"+gene+"/"+gene+"converted.phy"
#pathIn="C:/Users/Lena/Desktop/CXCR4.fasta"
#pathOut="C:/Users/Lena/Desktop/CXCR4-L.phy"

pathIn=arg.i
pathOut=arg.o
rmStop=arg.stop

fileData=open(pathIn,"r")
fileOut=open(pathOut,"w")
fileOutReport=open(pathOut.replace(".phy","-fasta2nucReport.txt"),"w")
logOut=open(pathOut.replace(".phy","-fasta2nucRmlog.txt"),"w")
#divide em sequencias
seq=string.replace(str(fileData.read()),"\r","")
seq=string.split(seq,">")
                 

seqCounter=0
for i in seq:
    if  len(i)>5:
        seqCounter=seqCounter+1
        ########cortar esta parte se for muito grande#### desempenho.....
        aux=string.split(i,"\n",1)
        aux=string.replace(aux[1],"\n","")
        print len(aux)
fileOut.write(" "+str(seqCounter)+" "+str(len(aux))+" \n")

seqN=0        
for i in seq:
    seqN+=1
    #Remove erros de artefactos devido à codificação de ficheiros ou sei lá do que é.
    if len(i)>5:
        #Divide as sequencias em nome e seq 
        org=string.split(i,"\n",1)
        org[1]=string.replace(org[1],"\n","")
        if len(org[0])>=10:
            if seqN<10:
                tmp=org[0][0:9]+"%s    " %(seqN)
                fileOut.write(tmp+"    ")
                fileOutReport.write(tmp+"--->"+org[0])
            else:
                tmp=org[0][0:8]+"%s    " %(seqN)
                fileOut.write(tmp)
                fileOutReport.write(tmp+"--->"+org[0])
        else:
            tmp=org[0][0:10]+"%s" %(seqN) 
            fileOut.write(tmp)
            fileOutReport.write(tmp+"--->"+org[0])
            xblanks=0
            if seqN<10:
            	xblanks=10-len(org[0])-1
            else:
                xblanks=10-len(org[0])-2
            for j in range(0,xblanks):
                fileOut.write(" ")
            fileOut.write("   ")        
        #Imprime sequencia
        for f in range(0,len(org[1]),3):
            if org[1][f:(f+3)].upper() in stop and rmStop:
                fileOut.write("---"+" ")
                countRm+=1
                logline = "Stop codon %s removed at pos %s in sequence: %s" %(org[1][f:(f+3)],f,org[0])
                print logline
                logOut.write(logline+"\n")
                logOut.flush()
                
            else:    
                fileOut.write(string.upper(org[1][f:(f+3)])+" ")
        fileOut.write("\n")
        fileOut.flush()
        fileOutReport.write("\n")
        fileOutReport.flush()
fileOut.flush()        
fileOut.close()
logOut.flush()
logOut.close()
fileOutReport.close()
print "%s codons removed" %(countRm)

        

