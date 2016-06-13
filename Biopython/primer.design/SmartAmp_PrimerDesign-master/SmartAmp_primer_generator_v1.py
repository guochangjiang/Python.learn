#!/usr/bin/python
# imports:
import operator
import sys
import random

# This lets raw_input do tab completion:
import readline
readline.parse_and_bind("tab: complete")

# SmartAmp primer generator v1
# Initially created 07-08-2014
# Sam Westreich
# OVERALL GOAL: Be able to select a raw sequence, and generate viable SmartAmp primers - no thought required!
###############################

# Part 1: input and checks
# This should get the initial input file, check for sequence length, & ensure that only bases are present.

print (" ")
print ("This is the primer generator for Smart Amplification, version 1.")
print ("At any time, press CTRL + C to cancel this script.")
print (" ")

print ("The input file must be only the raw bases.  Including flanking sequences, it must be at least 120 bases long to allow for primers to be generated.")
print (" ")

input_file_name = raw_input("Type in the name of the raw text document containing the target sequence and flanking sequences: ")

with open (input_file_name, "r") as myfile:
	raw_seq = myfile.read().replace("\n","")

if raw_seq.strip("GATC"):
	print ("\n File contains characters other than raw bases.")
	sys.exit()
else:
	print ("\n Sequence composition acceptable.\n")

if len(raw_seq) < 120:
	print ("Input sequence needs to be at least 120 characters in length.")
	sys.exit()
elif len(raw_seq) > 2000:
	print ("Your input sequence is greater than 2k bases; this may be too long for SmartAmp PCR.")
	sys.exit()
else:
	print ("Sequence length accepted.\n")
	
# Part 2: gathering all the parts of primers
# This should generate OP1 and OP2, and gather up the parts necessary to build FP and TP.

temp_OP1 = raw_seq[0:15]
OP1 = temp_OP1.replace('A','t').replace('T','a').replace('G','c').replace('C','g').upper()
print ("OP1 generated (5'-3'):\t\t\t" + OP1 )

temp_OP2 = raw_seq[-15:]
OP2 = temp_OP2.replace('A','t').replace('T','a').replace('G','c').replace('C','g').upper()
print ("OP2 generated (5'-3'):\t\t\t" + OP2 )

temp_TP = raw_seq[19:34]
TP_DS = raw_seq[55:70]

temp_FP = raw_seq[-34:-19]

# Part 3: building the turn-back primer (TP)
# This should generate complementary bases for TP, create the random filler bases, and then attach everything together to form the TP.

TP_conv = temp_TP.replace('A','t').replace('T','a').replace('G','c').replace('C','g').upper()

TP_rev = TP_conv[::-1]

TP_filler = ""
bases = "GATC"
for i in xrange(30):
	TP_filler += random.choice(bases)		# TP_filler is now a random set of bases 

str = ""
TP = str.join(TP_rev + TP_filler + TP_DS)
print ("Turn-back primer generated (5'-3'):\t" + TP)

# Part 4: building the folding primer (FP)
# This should generate complementary bases for FP, create the random filler bases, mirror them, and then attach everything together to form the FP.

FP_conv = temp_FP.replace('A','t').replace('T','a').replace('G','c').replace('C','g').upper()

FP_loopA = ""
for i in xrange(15):
	FP_loopA += random.choice(bases)
	
FP_loopB = FP_loopA.replace('A','t').replace('T','a').replace('G','c').replace('C','g').upper()[::-1]

FP = str.join(FP_loopA + FP_loopB + FP_conv)
print ("Folding primer generated (5'-3'):\t" + FP)