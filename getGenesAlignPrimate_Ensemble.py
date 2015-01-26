#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  getGenesAlignPrimate.py
#  
#  Copyright 2014 Bruno Costa <brunovasquescosta@gmail.com>
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
#  getGenesAlignPrimate.py v1.0
#  Author: Bruno Costa
#  Last update: 11/01/2014 
    
import argparse
import glob
import string
import re

parser = argparse.ArgumentParser(description="Remote tool to gather sequences of dna from seperate files")

parser.add_argument("-in",dest="infile", help="Provide the input file")
parser.add_argument("-OS",dest="OSsys",default="1", type=int, help="1:Linux;2:Windows;3:Mac")
parser.add_argument("-g", dest="gene", required=True, help="chose the gene sequence you want ot download")
parser.add_argument("-t", dest="target", default=0, help="Target length")
parser.add_argument("-var", dest="threshold",default=0, help="Target threshold for cut off sequence")
parser.add_argument("-rm", dest="rm_first", default=False, help="Remove following sequences. Used to remove sequences with similar length")
parser.add_argument("-all", dest="useAll", default=False, help="Used if interessed in using all species.")
arg = parser.parse_args()
##############PARAMETROS#################
##1:Linux
##2:Windows
##3:Mac
########GENE###
##gene="HOXB4"
OSsys=arg.OSsys
gene=arg.gene
target=int(arg.target)
threshold=float(arg.threshold)
rm_first=arg.rm_first
useAll=arg.useAll
########################### Lista de mamiferos   ###########################################################################

if(OSsys==1):
############################Linux####################################
    mammalian=open("primate list.txt", "r")
##########################windows####################################
if(OSsys==2):
    mammalian=open("c:/Documents and Settings/Lena/Documents/Tese Tymus/Python/primate list.txt", "r")
if(OSsys==3):
    mammalian=open("primate list.txt", "r")
mammal=mammalian.read().split("\n")
        
listMammal=[]
for i in range(0,len(mammal)):
    listMammal.append((mammal[i].split("\t")[0],1))
dMammal=dict(listMammal)

###########################||########||################||##################||################||#############################



########################### Nome Comum - Nome Cientifico ###################################################################
if(OSsys==1):
############################Linux####################################
    fTrad=open("/home/bcosta/Dropbox/Tese/Tese_Tymus/Python/translation.txt", "r")
##########################windows####################################
if(OSsys==2):
    fTrad=open("c:/Documents and Settings/Lena/Documents/Tese Tymus/Python/translation.txt", "r")
if(OSsys==3):
############################Linux####################################
    fTrad=open("translation.txt", "r") 

########################### GENE Transcript ###################################################################
if(OSsys==1):
############################Linux####################################
    trans=open("gene_transcript.txt", "r")
##########################windows####################################
if(OSsys==2):
    trans=open("c:/Documents and Settings/Lena/Documents/Tese Tymus/Python/gene_transcript.txt", "r")
if(OSsys==3):
############################Linux####################################
    trans=open("gene_transcript.txt", "r") 

trans=trans.read().split("\n")

translate_transcripts=[]
for t in trans:
    translate_transcripts.append(string.split(t,"\t"))

translate_transcripts=dict(translate_transcripts)
gene_trans=translate_transcripts[gene]

espTrad = fTrad.read().split("\n")
##for linux to get rid of the \r's##
aux=[]
for i in espTrad[:-1]:
    aux.append(i.replace("\r",""))
espTrad=aux

listaTrad=[]
for i in range(0,len(espTrad)-1):
    listaTrad.append(espTrad[i].split("\t"))
dTraducao=dict(listaTrad)
####### Foram colocados os termos num dicionario para trduzir nome comum para nome cientifico #######
########      Para inverter dictionario Cientifico para Comum    ###########################################
nomeC=list(dTraducao)
nomeCien=dict.values(dTraducao)
invTraducao=[]
for x in range(0,len(nomeC)):
    invTraducao.append([nomeCien[x],nomeC[x]])
invTraducao=dict(invTraducao)


#################################### -end invert- ############################################################

############################Linux####################################
if(OSsys==1):
    path="/home/bcosta/src/seq3/"
##########################windows####################################
if(OSsys==2):
    path="c:/Users/Lena/Documents/Tese Tymus/seq/"    
##################### on Mac ########################################
if(OSsys==3):
    path="../src/seq3/"
#print(path)



if useAll:
    listadir = glob.glob(path+gene_trans+"/ortholog_one2one/*/*")
    listadir = listadir + glob.glob(path+gene_trans+"/ortholog_one2one/*/*")
else:
    listadir = glob.glob(path+gene_trans+"/ortholog_one2one/Primates/*")
    listadir = listadir + glob.glob(path+gene_trans+"/ortholog_one2one/Haplorrhini/*")
#print listadir

if(OSsys==1):
############################Linux####################################
    fileWriter=open("/home/bcosta/Dropbox/Tese/Tese_Tymus/MAFFT_ENSEMBL/mafftAligncds"+gene+".fasta","w")
##########################windows####################################
if(OSsys==2):
    fileWriter=open("c:/Users/Lena/Documents/Tese_Tymus/MAFFT_ENSEMBL/mafftAligncds"+gene+".fasta","w")
if(OSsys==3):
############################Mac######################################
    fileWriter=open("../MAFFT_ENSEMBL1/mafftAligncds"+gene+".fasta","w")


############## Writes to file listed species ########################
global_avg=[0,0]
table=[]
removed=[]
tableCount=0
dub=dict()
for j in listadir:
    #print j
    #print path+gene+"/"

    order=string.rsplit(j,"/",1)[1]
    
    
    

    if(OSsys==1):
        #especieFile=string.replace(j,path+gene+"/","")
        especieFile=string.rsplit(j,"/",1)[1]
    if(OSsys==2):
        especieFile=string.rsplit(j,"\\",1)[1]
    if(OSsys==3):
        especieFile=string.rsplit(j,"/",1)[1]
    #removes [gene].txt    
    especieName=string.replace(especieFile,gene+".txt","")
    #print especieFile
    ##checks if file starts with a letter - Excludes check files
    if 1+1==2:##re.match("[A-Za-z]",especieFile[0]):
        
        ##checks if it's a mammal and writes it to the file

        try:
            if useAll:
		        print "all"
            else:
                dMammal[invTraducao[especieName]]
                  
            if 1+1==2:	
                c_name=invTraducao[especieName]
                fileGene=open(j,"r")
                #print(path+gene+"/"+especieFile)
                seq=fileGene.read()
                str(seq)
                l=string.split(seq, ">"  )
                local_avg=[0,0] #len(sequence),+1
                
                for sq in l[1:]:
                    header=string.split(sq,"\n")[0]
                    sequence=string.split(sq,"\n")[1]
                    if len(sequence)>3:

                        if re.search("N",string.split(sq,"\n")[1])==None:
                            if target == 0:
                                local_avg[0]+=len(sequence)
                                local_avg[1]+=1
                                global_avg[0]+=len(sequence)
                                global_avg[1]+=1
                                table.append([c_name[0:10],len(sequence)])
                                fileWriter.write(">"+invTraducao[especieName][0:10]+" "+sq)
                                fileWriter.flush()
                                if (local_avg[1]>1):
                                    print c_name+": this seq has a %s length. The %s average is %s the global average is %s\n%s" %(len(sequence),c_name,local_avg[0]/local_avg[1],local_avg[0]/local_avg[1],header)
                                else:
                                    tableCount+=1
                            else: #If target is set
                                if (len(sequence)>(target-target*threshold)) and (len(sequence)<(target*(threshold+1))):
                                    local_avg[0]+=len(sequence)
                                    local_avg[1]+=1
                                    global_avg[0]+=len(sequence)
                                    global_avg[1]+=1
                                    
                                    #print "%s with %s" %(c_name, len(sequence))
                                    
                                    if (local_avg[1]>1): #
                                        if (rm_first==False):
                                            fileWriter.write(">"+invTraducao[especieName][0:10].upper()+"\n"+sequence+"\n")
                                            fileWriter.flush()
                                            table.append([c_name[0:10],len(sequence)])
                                    else:
                                        if (rm_first):
                                            try: #Test this name
                                                dub[c_name[0:10]]
                                            except:#If name doesn't exist in dict write it else is not written  
                                                tableCount+=1
                                                dub[c_name[0:10]]=1
                                                table.append([c_name[0:10],len(sequence)])
                                                fileWriter.write(">"+invTraducao[especieName][0:10].upper()+"\n"+sequence+"\n")
                                                fileWriter.flush()      
                                        else:      #for rm_first false: Not sure if is used but might be a comb in which it's used
                                            tableCount+=1
                                            table.append([c_name[0:10],len(sequence)])
                                            fileWriter.write(">"+invTraducao[especieName][0:10].upper()+"\n"+sequence+"\n")
                                            fileWriter.flush()        

                        else:
                            removed.append(invTraducao[especieName])
                            print invTraducao[especieName]+" removed due to ambigous nucleotide base."    
                
        except KeyError:
               print(especieName +":  Sequence not copied. - exception KeyError found")
print "----------------------"
for all in table:
    print "|%s%s\t|%s|" %(all[0],(10-len(all[0]))*" ",all[1])
print "----------------------"
print "%s species." %(tableCount)
print "%s entries." %(len(table))
for all in removed:    
    print all+" removed"

fileWriter.flush()
fileWriter.close()


##for j in range(0,len(listadir)):
    ##especieFile = string.replace(listaespecie[j], path)


    ##+gene+"\\", "")
