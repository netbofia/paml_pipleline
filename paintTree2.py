#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  paintTree.py
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
#  paintTree.py v1.0
#  Author: Bruno Costa
#  Last update: 11/01/2014

import argparse
import glob
import string
import re

parser = argparse.ArgumentParser(description="Remote tool to paintTree structures according to selection through nodes")

parser.add_argument("-f",dest="infile", help="Provide the input file")
parser.add_argument("-OS",dest="OSsys",default="3", type=int, help="1:Linux;2:Windows;3:Mac")
parser.add_argument("-wdir",dest="dir", help="Can be used for non-standard files")
parser.add_argument("-r",dest="run", help="none - paint, 2- Tree search distance(branches away).")
###########################
arg = parser.parse_args()

##############PARAMETROS#################
##1:Linux
##2:Windows
##3:Mac

#########TEST################
#infile="/Users/bcosta/Dropbox/Tese/Tese Tymus/Results/paml/*PrimateRef2/wtree-*.tree"
#run=None
#wdir=None
#############################

###########################
infile=arg.infile
#OSsys=arg.OSsys
wdir=arg.dir
run=arg.run

class node(object):
    def __init__(self):
        self.name=None
        self.node=[]
        self.w=0
        self.d=0
        self.color=None
        self.prev=None
    def seg(self,child):
        "Gets a node by number"
        return self.node[child]
    def prev(self):
        self=self.prev
    def goto(self,data):
        "Gets the node by name"
        for child in range(0,len(self.node)):
            if(self.node[child].name==data):
                return self.node[child]
    def add(self):
        node1=node()
        self.node.append(node1)
        node1.prev=self
        return node1

class walk(object):
    def __init__(self,seq):
        #print "Starting to walk tree"
        self.tree=node()
        self.tree.name="root"
        self.outputTree="begin trees;\n\ttree tree_1 = [&R] "
        self.species=[]
        self.debug=False
        self.lBracket(seq)
    def lBracket(self, seq):
        l=seq.split("(")
        for b in l[0:-1]:
            if len(b.split(")"))==1:
                if re.match(".*[a-zA-Z0-9]+.*",b):
                    if self.debug:
                        print",- "+b
                    self.comma(b)
            if len(b.split(")"))>1:
                if self.debug:
                    print ")- "+b
                self.rBracket(b)
            self.outputTree+="("
            self.tree=self.tree.add()
        if len(l[-1].split(")"))==1:
            if re.match(".*[a-zA-Z0-9]+.*",l[-1]):
                self.comma(l[-1])
        if len(l[-1].split(")"))>1:
                self.rBracket(l[-1])

    def rBracket(self, seq):
        r=seq.split(")")
        for b in r[0:-1]:
            if re.match(".*[a-zA-Z0-9]+.*",b):
                if self.debug:
                    print ",-"+b
                self.comma(b)
            if self.tree.prev is not None:
                self.tree=self.tree.prev
                self.outputTree+=")"
        if re.match(".*[a-zA-Z0-9]+.*",r[-1]):
                if self.debug:
                    print ",-"+r[-1]
                self.comma(r[-1])
    def comma(self, seq):
        consec=False
        for c in seq.split(","):
            if consec:
                self.outputTree+=","
                if self.tree.prev is not None:
                    self.tree=self.tree.prev
                self.tree=self.tree.add()
            if re.match(".*[a-zA-Z]+.*",c):
                #if is a species leaf
                leaf=c.replace(" ","").split("#")
                self.outputTree+="\'"+leaf[0].split(":")[0]
                self.species.append(leaf[0].split(":")[0]+" "+"#"+leaf[1])
                self.tree.name=leaf[0].split(":")[0]
                self.tree.w=float(leaf[1])
                self.tree.d=float(leaf[0].split(":")[1])
            if re.match(".*[0-9]+.*",c):
                leaf=c.replace(" ","").split("#")
                if self.tree.name is None:
                    #print leaf[1]
                    self.outputTree+="[&w=\"#"+leaf[1]+"\","
                else:
                    self.outputTree+=" #"+leaf[1]+"\':"+str(self.tree.d)
                self.tree.w=float(leaf[1])
                self.tree.d=float(leaf[0].split(":")[1])
		self.color(leaf[1],self.tree.d)
                consec=True

    def color(self, seq, d):
        #coloring module for nexus output
        if float(seq)<=1:
            self.tree.color="blue"
            if self.tree.name is None:
                self.outputTree+="!hilight={"+str(self.branches(self.tree)+1)+",0.0,#-16763956}]:"+str(d)
		print 22+d
        else:
            self.tree.color="red"
            if self.tree.name is None:
                self.outputTree+="!hilight={"+str(self.branches(self.tree)+1)+",0.0,#-6750208}]:"+str(d)
		print d		
    def branches(self,node1):
        result=0
        tmp=len(node1.node)
        if tmp>0:
            result+=tmp-1
        for i in node1.node:
            result+=self.branches(i)
        return result
    def writeTree(self):
        self.outfile="#NEXUS\nbegin taxa;\n\tdimensions ntax=%s;\n\ttaxlabels" %(len(self.species))
        for i in self.species:
            self.outfile+="\n\t\'%s\'" %(i)
        self.outfile+="\n;\nend;\n\n%s;\nend;" %(self.outputTree)
        self.outfile+="""\n\nbegin figtree;\n\tset appearance.backgroundColorAttribute="Default";\n\tset appearance.backgroundColour=#-1;\n\tset appearance.branchColorAttribute="User selection";\n\tset appearance.branchLineWidth=1.0;\n\tset appearance.branchMinLineWidth=0.0;\n\tset appearance.branchWidthAttribute="Fixed";\n\tset appearance.foregroundColour=#-16777216;\n\tset appearance.selectionColour=#-2144520576;\n\tset branchLabels.colorAttribute="User selection";\n\tset branchLabels.displayAttribute="Branch times";\n\tset branchLabels.fontName="sansserif";\n\tset branchLabels.fontSize=8;\n\tset branchLabels.fontStyle=0;\n\tset branchLabels.isShown=false;\n\tset branchLabels.significantDigits=4;\n\tset layout.expansion=0;\n\tset layout.layoutType="RECTILINEAR";\n\tset layout.zoom=0;\n\tset legend.attribute="w";\n\tset legend.fontSize=10.0;\n\tset legend.isShown=false;\n\tset legend.significantDigits=4;\n\tset nodeBars.barWidth=4.0;\n\tset nodeBars.displayAttribute=null;\n\tset nodeBars.isShown=false;\n\tset nodeLabels.colorAttribute="User selection";\n\tset nodeLabels.displayAttribute="w";\n\tset nodeLabels.fontName="sansserif";\n\tset nodeLabels.fontSize=12;\n\tset nodeLabels.fontStyle=0;\n\tset nodeLabels.isShown=true;\n\tset nodeLabels.significantDigits=4;\n\tset nodeShape.colourAttribute="User selection";\n\tset nodeShape.isShown=false;\n\tset nodeShape.minSize=10.0;\n\tset nodeShape.scaleType=Width;\n\tset nodeShape.shapeType=Circle;\n\tset nodeShape.size=4.0;\n\tset nodeShape.sizeAttribute="Fixed";\n\tset polarLayout.alignTipLabels=false;\n\tset polarLayout.angularRange=0;\n\tset polarLayout.rootAngle=0;\n\tset polarLayout.rootLength=100;\n\tset polarLayout.showRoot=true;\n\tset radialLayout.spread=0.0;\n\tset rectilinearLayout.alignTipLabels=false;\n\tset rectilinearLayout.curvature=0;\n\tset rectilinearLayout.rootLength=100;\n\tset scale.offsetAge=0.0;\n\tset scale.rootAge=1.0;\n\tset scale.scaleFactor=1.0;\n\tset scale.scaleRoot=false;\n\tset scaleAxis.automaticScale=true;\n\tset scaleAxis.fontSize=8.0;\n\tset scaleAxis.isShown=false;\n\tset scaleAxis.lineWidth=1.0;\n\tset scaleAxis.majorTicks=1.0;\n\tset scaleAxis.origin=0.0;\n\tset scaleAxis.reverseAxis=false;\n\tset scaleAxis.showGrid=true;\n\tset scaleBar.automaticScale=true;\n\tset scaleBar.fontSize=9.0;\n\tset scaleBar.isShown=true;\n\tset scaleBar.lineWidth=7.0;\n\tset scaleBar.scaleRange=0.0;\n\tset tipLabels.colorAttribute="User selection";\n\tset tipLabels.displayAttribute="Names";\n\tset tipLabels.fontName="sansserif";\n\tset tipLabels.fontSize=12;\n\tset tipLabels.fontStyle=0;\n\tset tipLabels.isShown=true;\n\tset tipLabels.significantDigits=4;\n\tset trees.order=false;\n\tset trees.orderType="increasing";\n\tset trees.rooting=false;\n\tset trees.rootingType="User Selection";\n\tset trees.transform=false;\n\tset trees.transformType="cladogram";\nend;"""

    def t1(self, score, name1):
        #score is a 2D array and name1 is the name we are look for.
        #This function searches the tree for the specified species.
        # @return this function returns a 2D array with the tree at the target species and it's respective w
        if self.debug:
            print "1st - %s" %(score[0].name)
        if score[0].name==name1:
            score[1]=score[0].prev.w
            return score
        else:
            for t in score[0].node:
                result = self.t1([t,0],name1)
                if result[0].name==name1:
                    score=result
            if self.debug:
                print "2nd - %s" %(score[0].name)
            return score

    def t2(self,score,name2):
        #This method calculates the distance between both trees.
        #score is a 2D array and name2 is the species we are trying to get to.
        if self.debug:
            print "branch %s" %(score[0].name)
        if score[0].name==name2:
            if self.debug:
                print "1st - %s" %(score[0].name)
            return score
        else:

            for t in score[0].node:
                #get a method that only goes up!!!!! or it will be stuck in an infinite cycle
                if self.debug:
                    print "branch %s - up: %s" %(score[0].name,t.name)
                sendScore=score[1]+t.d
                result=self.up([t,sendScore],name2)
                if result[0].name==name2:
                    if self.debug:
                        print "branch %s - result %s" %(score[0].name,result[0].name)
                    score=result
            if score[0].name==name2:
                if self.debug:
                    print "2nd - %s" %(score[0].name)
                return score
            else:
                if self.debug:
                    print "3rd - %s" %(score[0].name)
                if score[0].prev is not None:
                    if self.debug:
                        print "3.5rd - %s - %s" %(score[0].name,score[0].prev.name)
                    sendScore=score[1]+score[0].d
                    result=self.t2([score[0].prev,sendScore],name2)
                    if result[0].name==name2:
                        if self.debug:
                            print "4rd - %s" %(score[0].name)
                        return result

    def up(self, score, name3):
        if self.debug:
            print "up %s" %(score[0].name)
        if score[0].name==name3:
            #This only happens when it finds the searched node
            #score[2]=score[0].prev.w
            return score
        else:
            for t in score[0].node:
                sendScore=score[1]+t.d
                result=self.up([t,sendScore],name3)
                if result[0].name==name3:
                    score=result
            return score
############Teste#############################
#infile="/Users/bcosta/Dropbox/Tese/Tese Tymus/Results/paml/*Primate/merged-*.tree"
#infile="../Results/paml/cd4Primate/wtree-cd4.tree"

#run=2
tree=None
fWriter=None
name1="Human"
name2="Gibbon"
species=["Human","Gibbon","Gorilla","Macaque","Orangutan","Chimpanzee","Sloth"]
#score=[[gene,w,w,distance]]
score1=[]
error1=[]
if run==2:
    #searches all trees in directory for distances
    for name1 in species:
        for name2 in species:

            if name1 <> name2:
                score1=[]
                error1=[]
                for i in glob.glob(infile):
                    if wdir is None:
                        tree=open(i,"r").read()
                    else:
                        tree=open(wdir+i,"r").read()
                    parse=walk(tree)
                    first1=parse.t1([parse.tree,0],name1)
                    first2=parse.t1([parse.tree,0],name2)

                    tree1=first1[0]
                    tree2=first2[0]

                    count1=0
                    count2=0

                    while tree1.name <> "root":
                        tree1=tree1.prev
                        count1+=1
                    while tree2.name <> "root":
                        tree2=tree2.prev
                        count2+=1

                    #print i.rsplit("/",2)[1].replace("Primate","")

                    try:
                        score1.append([i.rsplit("/",2)[1].replace("Primate",""),first1[1],first2[1],parse.t2([first1[0],0],name2)[1],count1,count2])
                    except TypeError:
                        error1.append(i.rsplit("/",2)[1].replace("Primate",""))
                        print i.rsplit("/",2)[1].replace("Primate","") + " has an error *************"

                print "%s vs. %s" %(name1,name2)
                for g,w1,w2,d,c1,c2 in score1:
                    if g not in error1:
                        print "%s\t%s\t%s\t%s\t%s\t%s" %(g,w1,w2,d,c1,c2)
                print ""

else:
    if wdir is None:
        tree=open(infile,"r").read()
        fWriter=open(infile.rsplit(".",1)[0]+".nexus","w")
    else:
        fWriter=open(wdir+infile.rsplit(".",1)[0]+".nexus","w")
        tree=open(wdir+infile,"r").read()
    parse=walk(tree)
    parse.writeTree()
    fWriter.write(parse.outfile)
    fWriter.flush()
    fWriter.close()
print infile+" :DONE"


