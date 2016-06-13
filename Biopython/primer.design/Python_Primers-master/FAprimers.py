#python script to pass sequences from fasta file to the command line primer designer, take the output and save it to a multi fasta fileno


import sys 
import Bio
import subprocess

def load_fasta(fastafile):
	filein = open(fastafile, 'r').readlines()
	for x in filein:
		x = x.replace('\n', '')
		if '>' in x:
			heads.append(x)
			add_seq = 'true'
		else:
			add_seq = 'false'
			seq_temp.append(x)
			
	for x in seq_temp:
		if 'g' in x or 'G' in x:
			seqs.append(x)
	
	global seq_dict
	seq_dict = dict()
	seq_dict = dict(zip(heads, seqs))
	
	print "HEADS" 
	print heads
	print "SEQS" 
	print seqs 
	print "SEQ_DICT:" 
	print seq_dict
	
def run_primers(gene, seq):
	test = ('python cl-primers-forfasta.py ' + seq)
	process = subprocess.Popen(test, shell=True, stdout=subprocess.PIPE)
	process.wait()
	#print process.returncode # 0 = success, optional check
	# read the result to a string
	output = process.stdout.read()
	print "----- Primers for " + gene + "- - - - - -"
	#print output
	output = output.split('\n')
	if 'G' in output[0]:
		print gene + ' left = ' + output[0]
		print gene + ' right = ' + output[2]
		primers_out.write(gene + ' left = ' + output[0] + "\n")
		primers_out.write(gene + ' right = ' + output[2] + "\n")

		
heads = list()
seq_temp = list()
seqs = list()
global seq_dict
seq_dict =  dict()

if (len(sys.argv) > 1):
	fasta_in = sys.argv[1]
	load_fasta(fasta_in)
else : 	
	fasta_in = prompt("What file do you want to use?")
	load_fasta(fasta_in)

seq_keys = seq_dict.keys()

primers_out = open("final_primers", 'w')

for k in seq_keys:
	run_primers(k, seq_dict[k])

