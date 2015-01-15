#!/bin/bash

#setting variables
#server="yamcha"
#server="trunks"
#server="krillin"
#server="philaenus"
server="philaenus2"
#server="tartarugagenial"
#session="tese"
session="tese1"


alias blasttese='/Users/bcosta/Dropbox/Tese/Tese_Tymus/Python/blast/./blast.py'
alias fasta2nuc='python2 /Users/bcosta/Dropbox/Tese/Tese_Tymus/Python/fasta2nuc.py'
alias getparam='python2 /Users/bcosta/Dropbox/Tese/Tese\ Tymus/getparam.py'
alias maffttese='cd ~/Dropbox/Tese/Tese_Tymus/MAFFT/'
alias pythontese='cd ~/Dropbox/Tese/Tese_Tymus/Python/'
alias resultstese='cd /Users/bcosta/Dropbox/Tese/Tese\ Tymus/Results/paml/'
alias xmlparser='python2 /Users/bcosta/Dropbox/Tese/Tese_Tymus/Python/xml\ parser.py'
alias transX="~/Dropbox/Tese/Tese_Tymus/Python/transX/transX.pl"
alias sshyamcha="ssh brunocosta@yamcha.alunos.fc.ul.pt"
alias sshphilaenus="ssh brunocosta@philaenus.alunos.fc.ul.pt"
alias sshkrillin="ssh brunocosta@krillin.alunos.fc.ul.pt"
alias resultspython='cd /Users/bcosta/Dropbox/Tese/Tese\ Tymus/Python/'

echo "Alias deployed"

while getopts "g:" flag
do
gene=$OPTARG
done

echo "$gene is being processed!"

#Steps 0:Get genes; 1:Blasting 2:Alignment 3:Tree; 4:Preparing Paml 5:Paml 6:Get Results 7:Process results
echo "What step?"
echo "0:Get genes" 
echo "1:Blasting "
echo "2:Alignment "
echo "3:Tree"
echo "4:Preparing Paml" 
echo "5:Paml"
echo "6:Get Results "
echo "7:Process results "
echo "8:wtree"

step=$(dd bs=1 count=1 2> /dev/null)

	#"0:Get genes" 
if [ "$step" -eq "0" ] 
	then
	pythontese
	python2 getGenesAlignMammal.py -g $gene &&
	maffttese &&
	mkdir $gene
	echo "dir created"
	read ss &&
	mv mafftAligncds$gene.fasta $gene
	cd $gene
	#tirar primeira linha do fasta Suponho que tenha de fazer um script em python #To do
        tail -n +2 mafftAligncds$gene.fasta>tmp.fasta &&
        mv tmp.fasta mafftAligncds$gene.fasta
	step=1
fi

	#"1:Blasting "
if [ "$step" -eq "1" ]
	then
	#Necessary for step jumping
	maffttese
	cd $gene
	echo "Blasting sequences"
	#Blasting
	ssh brunocosta@$server.alunos.fc.ul.pt "mkdir /home/brunocosta/paml4.6/$gene/"
	ssh brunocosta@$server.alunos.fc.ul.pt "mkdir /home/brunocosta/paml4.6/$gene/blast/"
	scp mafftAligncds$gene.fasta brunocosta@$server.alunos.fc.ul.pt:~/paml4.6/$gene/blast/
	runner="cd /home/brunocosta/paml4.6/$gene/blast/ && /home/brunocosta/Tools/blast_wrapper/./blast.py -in mafftAligncds$gene.fasta -b blastn -hit 1 -o blast$gene.xml -outfmt XML && ssh brunocosta@odin.fc.ul.pt python2 notify.py"
#	ssh brunocosta@$server.alunos.fc.ul.pt "screen -S tese1 -X stuff '$runner'"
	echo "Runing blast on $server. Continue?"
	read result &&
	scp brunocosta@$server.alunos.fc.ul.pt:~/paml4.6/$gene/blast/blast$gene.xml .
	#blasting works badly in script
	#blasttese -in mafftAligncds$gene.fasta -b blastn -hit 1 -o blast$gene.xml -outfmt XML &&
	xmlparser -in blast$gene.xml -g $gene >blast.txt &&
	pwd
	echo "Check result in blast.txt "
	result="n"
	while [ "$result" == "n" ]
	do
	echo "Type y to continue"
	result=$(dd bs=1 count=1 2> /dev/null)
	done
	step=2
fi


	#"2:Alignment "
if [ "$step" -eq "2" ]
	then
	#necessary for step jumping
	maffttese 
	pwd
	cd $gene
	pwd
	
	##Aligning with TransX in subfolder using Mafft
	mkdir transX 
	cd transX 
	pwd
	echo "Getting alignment with translatorX usinf mafft"
	transX -i ../mafftAligncds$gene.fasta -p F &&
	mv translatorx_res.nt_ali.fasta ../$gene.fasta
	cd .. &&
	
	#Convert to phy alignment
	fasta2nuc -i $gene.fasta -o $gene.phy -s True
	step=3
fi

	#"3:Tree"
if [ "$step" -eq "3" ]
	then
	#Necassery for step jumping
	echo "Making tree"
	maffttese &&
	cd $gene
	ssh brunocosta@$server.alunos.fc.ul.pt "mkdir paml4.6/$gene"
	scp $gene.* brunocosta@$server.alunos.fc.ul.pt:~/paml4.6/$gene
	
	echo "Files sent to server starting tree"
	#RaXml
	insert="cd /home/brunocosta/paml4.6/$gene/ && mkdir tree && cd tree && /home/brunocosta/Tools/standard-RAxML-master/raxmlHPC-PTHREADS-SSE3 -T 4 -n tree -s ../$gene.phy -N 1000 -m GTRCAT -p 12345672290 && cp RAxML_bestTree.tree ../$gene.tree && ssh brunocosta@odin.fc.ul.pt python2 notify.py"
	echo "$insert"
	ssh brunocosta@$server.alunos.fc.ul.pt "screen -S $session -X stuff '$insert'"
	#ssh brunocosta@$server.alunos.fc.ul.pt "screen -R && cd ~/paml4.6/$gene/ && mkdir tree && cd tree;/home/brunocosta/Tools/standard-RAxML-master/raxmlHPC-PTHREADS-SSE3 -T 4 -n tree -s ../$gene.phy -N 1000 -m GTRCAT -p 12345672290 && cp RAxML_bestTree.tree ../$gene.tree"		
	step=4
	result="n"
	while [ "$result" == "n" ]
	do
	echo "Type y to continue"
	result=$(dd bs=1 count=1 2> /dev/null)
	done
	
fi

	#"4:Preparing Paml"
if [ "$step" -eq "4" ]
	then
	echo "4:Preparing Paml" 
	#Retreive tree from $server to (root it?) 
	maffttese &&
	cd $gene
	scp brunocosta@$server.alunos.fc.ul.pt:~/paml4.6/$gene/$gene.tree .
	pwd
	echo "Open tree in Figtree set it right and export as newick tree set to current tree (crl+r)"

	result2="n"
	while [ "$result2" == "n" ]
	do
	echo "Type y to continue"
	result2=$(dd bs=1 count=1 2> /dev/null)
	done
	read result3 &&
	
	#Open it with fig tree
	#and send it back to $server
	scp $gene.tree brunocosta@$server.alunos.fc.ul.pt:~/paml4.6/$gene/
	
	#Creates dirs
	for i in 0 1 2 3 7 8 wtree
	do
	ssh brunocosta@$server.alunos.fc.ul.pt "cd paml4.6/$gene/ && mkdir m$i"
	done
	
	#Creates the codml.ctl for each folder
	#Makes the control files for paml
	ssh brunocosta@$server.alunos.fc.ul.pt "Tools/./ctlMaker.py -wdir paml4.6/$gene/ -g $gene"
	echo "Start screens on sever $server [0/1]"
	read srtScreen &&
	if [ "$srtScreen" -eq "1" ] 
		then 
		ssh brunocosta@$server.alunos.fc.ul.pt "screen -S tese1"
		ssh brunocosta@$server.alunos.fc.ul.pt "screen -S tese2"
		ssh brunocosta@$server.alunos.fc.ul.pt "screen -S tese3"
		ssh brunocosta@$server.alunos.fc.ul.pt "screen -S tese4"
	fi
	step=5
fi
	#"5:Paml"
if [ "$step" -eq "5" ]
	then
	#Runs codeml for all
	echo "Starting to run codeml. Continue?"
	read result &&
	#I really don't care what the result is just want it to wait HA HA HA
	ssh brunocosta@$server.alunos.fc.ul.pt "sh /home/brunocosta/Tools/codeml_teste -g $gene" && 
	echo "Running codeml in screen. Continue[0/1]?"
	read result &&
	if [ "$result" -eq "1" ]
		then
		step=6
		else
		exit 0
	fi
fi

if [ "$step" -eq "6" ]; then
	#Fetch results
	mkdir ~/Dropbox/Tese/Tese\ Tymus/Results/paml/$gene
	for i in 0 1 2 3 7 8 wtree
	do
	scp brunocosta@$server.alunos.fc.ul.pt:/home/brunocosta/paml4.6/$gene/m$i/Results_m$i.txt ~/Dropbox/Tese/Tese\ Tymus/Results/paml/$gene/
	done
	scp brunocosta@$server.alunos.fc.ul.pt:/home/brunocosta/paml4.6/$gene/m3/rst ~/Dropbox/Tese/Tese\ Tymus/Results/paml/$gene/rst_m3.txt
	step=7
fi

if [ "$step" -eq "7" ]; then
	#Process results
	resultstese
	cd ../../Python
	python2 getparam.py -g $gene &&
	echo "Parse File ok"
	cat ../Results/paml/$gene/parse.txt
	java -jar writeparam.jar $gene
fi

if [ "$step" -eq "8" ]; then
	#Fetch results
	
	mkdir ~/Dropbox/Tese/Tese\ Tymus/Results/paml/$gene
	
	scp brunocosta@$server.alunos.fc.ul.pt:/home/brunocosta/paml4.6/$gene/m$i/Results_m$i.txt ~/Dropbox/Tese/Tese\ Tymus/Results/paml/$gene/
	
fi

exit 0
