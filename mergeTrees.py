#!/usr/bin/env python2
__author__ = 'bcosta'



import glob
import re

type="Primate"
type="Ensembl"

#type="1 wtree 2 M2ns0 -target"
run=1

#dTreeDir="../../Tese_Tymus/MAFFT/*Primate/*.tree"
#wTreeDir="../Results/paml/*PrimateRef2/wtree-*.tree"

#File input for glob
resultsPaml="../Results/paml/*"+type
#test
#resultsPaml="../Results/paml/FOXN1Ensembl"

#dTrees=glob.glob(dTreeDir)

genes=glob.glob(resultsPaml)
for i in genes:
    print i	
    run=1
    gene=i.rsplit("/",1)[1].replace(type,"")
    try:
	dTree=open(i+"/"+gene+".tree","r")
	dTree=dTree.read()
    except:
	run=0
	print gene+" error"
    if run==1:
    	wTree=open(i+"/wtree-"+gene+type+".tree","r")
    if run==2:
        wTree=open(i+"/wtree-"+gene+"-M2ns0.tree","r")

    #for j in test:
        #if j.rsplit("/",1)[1].replace(".tree","")<>gene:
    #dTree=open(j,"r")
    print run
    if run<> 0:
	wTree=wTree.read()
	#print j 
	       
	wTree=wTree.replace(" ","")
	dTree=dTree.replace(" ","")
	
	dSplits=dTree.split(")")
	wSplits=wTree.split(")")
	tree=wSplits[0]
	
	for k in range(1,len(dSplits)):
	    try:
	        tree+= ")"+dSplits[k].split(",")[0]+wSplits[k]
	    except:
	        print gene+" - error"
	for k in re.findall("[A-Za-z_]+:[0-9]+.[0-9]+",dTree):
	    tree=tree.replace(k.split(":")[0],k)
	
	#print "dTree "+ dTree
	#print "wTree "+ wTree
	tree=tree.replace(":0.0;",";").replace(";\n;",";")
	print gene+" - "+tree
    if run==1:
        w=open(i+"/merged-wtree-"+gene+".tree","w")
    if run==2:
        w=open(i+"/merged-wtree-"+gene+"-M2ns0.tree","w")
    if run<>0:
        w.write(tree)
        w.flush()
        w.close()


