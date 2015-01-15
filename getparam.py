#!/usr/bin/python2.7
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  getparam.py
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
#  getparam.py v1.0
#  Author: Bruno Costa
#  Last update: 27/01/2014

import argparse

parser = argparse.ArgumentParser(description="Remote tool to get parameters from results of paml to parse.txt")
parser.add_argument("-g",dest="gene", required=True, help="Choose the gene sequence you want to fetch")

arg = parser.parse_args()

import string
import re
gene=arg.gene
output="/Users/bcosta/Dropbox/Tese/Tese Tymus/Results/paml/"+gene+"/parse.txt"
saida=open(output,"w")
ajusteLn=1
ajustedNdS=1
pasta="/Users/bcosta/Dropbox/Tese/Tese Tymus/Results/paml/"+gene
######################model 0###########################################
path=pasta+"/Results_m0.txt"
saida.write("###model0###")
model=open(path,"r")
model=model.read()
model0=string.split(model,"\n")
counter=0
for line in model0:
    if re.match("lnL*",line):
        print line
        #print string.split(line," ")
        for lNmatch in line.split(" "):
            if re.match('-|\+',lNmatch):
                print lNmatch
                saida.write("\n"+string.replace(lNmatch,".",","))
                break

    if re.match("Detailed output identifying parameters",line):
        print model0[counter+2] #kappa
        saida.write("\n"+string.replace(string.split(model0[counter+2]," ")[4],".",","))
        print model0[counter+4] #w
        saida.write("\n"+string.replace(string.split(model0[counter+4]," ")[4],".",","))
        print "############ Model 1 ###########"
    counter+=1        
saida.flush()
######################model 1###########################################
path=pasta+"/Results_m1.txt"
saida.write("\n###model1###")
model=open(path,"r")
model=model.read()
model1=string.split(model,"\n")
counter=0
for line in model1:
    if re.match("lnL*",line):
        print line
        for lNmatch in line.split(" "):
            if re.match('-|\+',lNmatch):
                print lNmatch
                saida.write("\n"+string.replace(lNmatch,".",","))
                break
    if re.match("Detailed output identifying parameters",line):
        print model1[counter+2] #kappa
        saida.write("\n"+string.replace(string.split(model1[counter+2]," ")[4],".",","))
        print model1[counter+7] #parameters
        saida.write("\n"+string.replace(string.split(model1[counter+7]," ")[3],".",","))
        saida.write("\t"+string.replace(string.split(model1[counter+7]," ")[5],".",","))        
        print model1[counter+8] #w
        element=0
        for w1 in string.split(model1[counter+8]," "):
            if re.match('[0-9]',w1):
                element+=1
                if element==1:
                    saida.write("\n"+string.replace(w1,".",","))
                else:
                    saida.write("\t"+string.replace(w1,".",","))                    
        print model1[counter+12]
        print model1[counter+14] #dn/dS        
        element=0
        for dnds in string.split(model1[counter+14]," "):
            if re.match('[0-9]',dnds):
                element+=1
            if element==5:
                print dnds
                saida.write("\n"+string.replace(dnds,".",","))        
                break
        print "########### Model 2 ############"
    counter+=1        
saida.flush()
######################model 2##############################################
path=pasta+"/Results_m2.txt"
saida.write("\n###model2###")
model=open(path,"r")
model=model.read()
beb2=[]
model2=string.split(model,"\n")
counter=0
for line in model2:
    if re.match("lnL*",line):
        print line
        for lNmatch in line.split(" "):
            if re.match('-|\+',lNmatch):
                print lNmatch
                saida.write("\n"+string.replace(lNmatch,".",","))
                break
    if re.match("Detailed output identifying parameters",line):
        print model2[counter+2] #kappa
        saida.write("\n"+string.replace(string.split(model2[counter+2]," ")[4],".",","))
        print model2[counter+7] #parameters
        saida.write("\n"+string.replace(string.split(model2[counter+7]," ")[3],".",","))
        saida.write("\t"+string.replace(string.split(model2[counter+7]," ")[5],".",","))
        saida.write("\t"+string.replace(string.split(model2[counter+7]," ")[7],".",","))                
        print model2[counter+8] #w
        element=0
        for w1 in string.split(model2[counter+8]," "):
            if re.match('[0-9]',w1):
                element+=1
                if element==1:
                    saida.write("\n"+string.replace(w1,".",","))
                else:
                    saida.write("\t"+string.replace(w1,".",","))   
        #print string.split(model2[counter+8]," ")  # Para conferir tirar #
        print model2[counter+12] 
        print model2[counter+16] #dn/ds
        print string.split(model1[counter+16]," ")
        print string.replace(string.split(model2[counter+16]," ")[19+ajustedNdS],".",",")
        element=0
        for dnds in string.split(model2[counter+14]," "):
            if re.match('[0-9]',dnds):
                element+=1
            if element==5:
                print dnds
                saida.write("\n"+string.replace(dnds,".",","))        
                break      
        print counter
    if re.match("Bayes Empirical Bayes \(BEB\) analysis \(Yang, Wong & Nielsen 2005\. Mol\. Biol\. Evol\. 22\:1107-1118\)",line):
        if re.match("Positively selected sites*",model2[counter+1]):
            counter+=6
            while re.match("  *",model2[counter]):
                print model2[counter]
                beb2.append(model2[counter])
                counter+=1
            print "##########Model 3#############"
    counter+=1        
saida.flush()
######################model 3##############################################
path=pasta+"/Results_m3.txt"
saida.write("\n###model3###")
model=open(path,"r")
model=model.read()
neb3=[]
model3=string.split(model,"\n")
counter=0
for line in model3:
    if re.match("lnL*",line):
        print line
        for lNmatch in line.split(" "):
            if re.match('-|\+',lNmatch):
                print lNmatch
                saida.write("\n"+string.replace(lNmatch,".",","))
                break
    if re.match("Detailed output identifying parameters",line):
        print model3[counter+2] #kappa
        saida.write("\n"+string.replace(string.split(model3[counter+2]," ")[4],".",","))
        print model3[counter+7] #parameters
        saida.write("\n"+string.replace(string.split(model3[counter+7]," ")[3],".",","))
        saida.write("\t"+string.replace(string.split(model3[counter+7]," ")[5],".",","))
        saida.write("\t"+string.replace(string.split(model3[counter+7]," ")[7],".",","))                
        print model3[counter+8] #w
        element=0
        for w1 in string.split(model3[counter+8]," "):
            if re.match('[0-9]',w1):
                element+=1
                if element==1:
                    saida.write("\n"+string.replace(w1,".",","))
                else:
                    saida.write("\t"+string.replace(w1,".",","))          
        print model3[counter+12] 
        print model3[counter+14] #dn/ds
        element=0
        for dnds in string.split(model3[counter+14]," "):
            if re.match('[0-9]',dnds):
                element+=1
            if element==5:
                print dnds
                saida.write("\n"+string.replace(dnds,".",","))        
                break
        print "##########model 7#############"
    if re.match("Naive Empirical Bayes \(NEB\) analysis",line):
        if re.match("Positively selected sites*",model3[counter+1]):
            counter+=6
            while re.match("  *",model3[counter]):
                print model3[counter]
                neb3.append(model3[counter])           
                counter+=1
    counter+=1        
saida.flush()
######################model 7##############################################
path=pasta+"/Results_m7.txt"
saida.write("\n###model7###")
model=open(path,"r")
model=model.read()
model7=string.split(model,"\n")
counter=0
for line in model7:
    if re.match("lnL*",line):
        print line
        for lNmatch in line.split(" "):
            if re.match('-|\+',lNmatch):
                print lNmatch
                saida.write("\n"+string.replace(lNmatch,".",","))
                break
    if re.match("Detailed output identifying parameters",line):
        print model7[counter+2] #kappa
        saida.write("\n"+string.replace(string.split(model7[counter+2]," ")[4],".",","))        
        print model7[counter+5] #parameters
        saida.write("\n"+string.replace(string.split(model7[counter+5]," ")[5],".",","))
        saida.write("\t"+string.replace(string.split(model7[counter+5]," ")[11],".",",")) 
        print model7[counter+15] 
        print model7[counter+17] #dn/ds
        element=0
        for dnds in string.split(model7[counter+17]," "):
            if re.match('[0-9]',dnds):
                element+=1
            if element==5:
                print dnds
                saida.write("\n"+string.replace(dnds,".",","))        
                break
        print "##########model 8#############"
    counter+=1
saida.flush()
######################model 8##############################################
path=pasta+"/Results_m8.txt"
saida.write("\n###model8###")
model=open(path,"r")
model=model.read()
beb8=[]
model8=string.split(model,"\n")
counter=0
for line in model8:
    if re.match("lnL*",line):
        print line
        for lNmatch in line.split(" "):
            if re.match('-|\+',lNmatch):
                print lNmatch
                saida.write("\n"+string.replace(lNmatch,".",","))
                break
    if re.match("Detailed output identifying parameters",line):
        print model8[counter+2] #kappa
        saida.write("\n"+string.replace(string.split(model8[counter+2]," ")[4],".",","))        
        print model8[counter+5] #parameters
        saida.write("\n"+string.replace(string.split(model8[counter+5]," ")[6],".",","))
        saida.write("\t"+string.replace(string.split(model8[counter+5]," ")[12],".",","))
        saida.write("\t"+string.replace(string.split(model8[counter+5]," ")[17],".",","))                
        print model8[counter+6] #w
        parm2M8=string.replace(model8[counter+6]," ","").split(")")
        first=parm2M8[0].split("=")[1]
        second=parm2M8[1].split("=")[1]        
        saida.write("\n"+first) 
        saida.write("\t"+second)        
        print model8[counter+18]
        print model8[counter+20]
        element=0
        for dnds in string.split(model8[counter+20]," "):
            if re.match('[0-9]',dnds):
                element+=1
            if element==5:
                print dnds
                saida.write("\n"+string.replace(dnds,".",","))        
                break
        print "#######################"
    if re.match("Bayes Empirical Bayes \(BEB\) analysis \(Yang, Wong & Nielsen 2005\. Mol\. Biol\. Evol\. 22\:1107-1118\)",line):
        if re.match("Positively selected sites*",model8[counter+1]):
            counter+=6
            while re.match("    *",model8[counter]):
                print model8[counter]
                beb8.append(model8[counter])
                counter+=1
    counter+=1            
saida.flush()
saida.write("\nBaysien totals")
saida.write("\n"+str(len(beb2))+"\t"+str(len(neb3))+"\t"+str(len(beb8)))
saida.write("\n######")
saida.write("\nBEB Model 2")
for i in beb2:
    saida.write("\n"+i)
saida.write("\n######")
saida.write("\nNEB model 3")
for i in neb3:
    saida.write("\n"+i)
saida.write("\n######")    
saida.write("\nBEB Model 8")
for i in beb8:
     saida.write("\n"+i)
     saida.flush()
saida.close()
