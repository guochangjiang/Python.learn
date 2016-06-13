#!/usr/bin/env python
import sys
from Bio import SeqIO
import subprocess 


def change_chars(sequence): 
			chars_to_change = ['q','w','e','r','y','u','i','o','p','s','d','f','h','j','k','l','z','x','v','b','n','m','Q','W','E','R','Y','U','I','O','P','S','D','F','G','H','J','K','L','Z','X','V','B','N','M']
			for index, char in enumerate(sequence):
				sequence = sequence.replace(char, 'N')   
			print index 
			return sequence

def write_primer3_input(sequence):    
		if sequence == 'null':
			print "USING EXAMPLE SEQUENCE: "
			sequence = "aggctvagctagcatcgatcagactagctacacttacgactacgactacgtactcagatcagtacgactacgactacgcatcgcatcatacgcatacgactacacactacgatcatctatcatcagtcgactacgtcgctagctagctacgac"
			gene = 'recG'
			print '\nGenerating primer3 input file from example sequence:  ' + sequence
		elif len(sequence) > 30:
			print '\nGenerating primer3 input file with submitted sequence:  ' + sequence
    	
		newseq = str()
		#FORMAT SEQUENCE TO TURN ANYTHING NOT A, T, G, OR C INTO N
		chars_to_change = ['q','w','e','r','y','u','i','o','p','s','d','f','h','j','k','l','z','x','v','b','n','m','Q','W','E','R','Y','U','I','O','P','S','D','F','G','H','J','K','L','Z','X','V','B','N','M']
		for index, char in enumerate(sequence):
			if char in chars_to_change:
				newseq = newseq + 'N'   
			else:
				 newseq = newseq + char         	
		#Loads default primer3 options
		primer3options = open('./primer3/cloning_primer3_options.txt').readlines()  
		
		print newseq
		#CONSTRUCT PRIMER3 OPTIONS FILE, RUN PRIMER3 AND SAVE FILE TO primer3_input
		product_size = len(sequence)
		prod_size_w_BB = len(sequence) + 55
		print "\n Projected Product Size is " + str(product_size) + 'bp ( ' + str(prod_size_w_BB) + 'bp with Biobrick adapters )\n'                
		end_base = str (product_size)
		
		sequence_template = "SEQUENCE_TEMPLATE=" + sequence + "\n"
		target = "SEQUENCE_INCLUDED_REGION=0, " + end_base + "\n"
			
		output = open('./primer3/primer3_input', 'w')
		output.write(sequence_template)
		output.write(target)
		for x in primer3options:
			output.write(x)
			
    #END write_primer3_input





def run_primer3(): 
	print "- - - - - - - Running Primer3 - - - - - - - \n"
	test = ('./primer3/primer3_core' + ' ./primer3/primer3_input')
	process = subprocess.Popen(test, shell=True, stdout=subprocess.PIPE)
	process.wait()
	#print process.returncode # 0 = success, optional check
	# read the result to a string
	primer3 = process.stdout.read()

	#print primer3		#  ------ PRINT PRIMER 3 OUTPUT -------
	
	primer3_outfile = open('./primer3/primer3_output.txt', 'w')
	primer3_outfile.write(primer3)
	primer3_outfile.close()
    
	primer3_out = primer3.split('\n')

    #BEGIN TO LOOSEN THRESHOLDS IF PRIMER3 DOESN'T FIND ANY PRIMERS - ADD PARAMETERS OTHER THAN Tm?

	while primer3_out[len(primer3_out) - 1] == 0:
                    print "\nReworking primer3 parameters\n\n"
            
                    primer3_input = open("/primer3/primer3_input").readlines().split('\n')
                    close('/primer3/primer3_input')
                    
                    #SHIFT Tms OUT ONE DEGREE EVERY IT.- MAKE MORE RESPONSIVE BY ONLY SHIFTING TROUBLING PARAMETER
                    starting_primer_min_tm = primer3_input[9][-3:-1]
                    starting_primer_max_tm = primer3_input[11][-3:2]
                    next_primer_min_tm = starting_primer_min_tm[:-1]
                    next_primer_max_tm = starting_primer_min_tm[1:]
                    print "Changing Primer_Min_Tm from %s to %n \n" %(starting_primer_min_tm, next_primer_min_tm)
                    print "Changing Primer_Max_Tm from %s to %n \n" %(starting_primer_max_tm, next_primer_max_tm)
                            
                    primer3_input[12] = "PRIMER_MIN_TM=%n\n" % next_primer_product_min_tm
                    primer3_input[13] = "PRIMER_MAX_TM=%n\n" % next_primer_product_max_tm
            
                    starting_primer_product_min_tm = primer3_input[12][-3:-1]
                    starting_primer_product_max_tm = primer3_input[13][-3:-1]
                    next_primer_product_min_tm = starting_primer_product_min_tm[:-1]
                    next_primer_product_max_tm = starting_primer_product_max_tm[1:]
                    print "Changing Primer_Product_Min_Tm from %s to %n \n" % (starting_primer_product_min_tm, next_primer_product_min_tm)
                    print "Changing Primer_Product_Max_Tm from %s to %n \n" % (starting_primer_product_max_tm, next_primer_product_max_tm)
                    primer3_input[12] = "PRIMER_PRODUCT_MIN_TM=%n\n" % (next_primer_product_min_tm)
                    primer3_input[13] = "PRIMER_PRODUCT_MAX_TM=%n\n" % (next_primer_product_max_tm)
                
            #REWRITE PRIMER3_INPUT FILE WITH NEW Tm PARAMETERS
                    output = open ("/primer3/primer3_input", 'w')
                    output.write(primer3_input)
                    output.close()

            #IF PRIMERS ARE FOUND, PRIMER3 OUTPUT IS APPENDED TO PRIMER3_OUTPUT
                    #print "PRIMER3 OUTPUT FOR %i: \n\n" % id
                    #print "\n\nPRIMER3 OUTPUT for %i: \n\n" % id
                    #print primer3_out
                    #print primer3_out
    
    
                    close("/primer3/primer3_input")
                    #END run_primer3



def extract_primer_sequences(): #SUBROUTINE
		primer3_output = open("./primer3/primer3_output.txt", 'r').readlines()
		final_primers = open("final_primers.fa", 'w')
        
		for line in primer3_output:
			if line[:22] == 'PRIMER_LEFT_0_SEQUENCE':
					left = line
					left = left[23:]
					#print 'Left Primer: ' + left	
			if line[:23] == 'PRIMER_RIGHT_0_SEQUENCE':
					right = line
					right = right[24:]
					#print 'Right Primer: ' + right
	 		if line[:22] == 'PRIMER_LEFT_0_PROBLEMS':
					left_problems = line[23:]
			if line[:23] == 'PRIMER_RIGHT_0_PROBLEMS':
					right_problems = line[24:]

		#Ensure variables are defined, if not label as 'none'					
		try:
			left
		except NameError:
			left = 'none'
		try:
			right
		except NameError:
			right = 'none'
		try:
			left_problems
		except NameError:
			left_problems = 'none'
		try:
			right_problems
		except NameError:
			right_problems = 'none'
			            
		if left_problems != 'none' and right_problems != 'none':
				print "Made the best primers possible, but there might still be some issues:\n"
		if left_problems != 'none':
				print "Potential problems with the left primer: " + left_problems
		if right_problems != 'none':
				print "Potential problems with the right primer: " + right_problems
		
		print "- - - - - - Primer Sequences - - - - - - \n"		
		if left != 'none' and right != 'none':
			print "Sense_Primer: " + left
			print "Aintisense_Primer: " + right
			final_primers.write('Sense Primer: ' + left)
			final_primers.write('Antisense Primer: ' + right)
	 		

                        
		final_primers.close()
		
# 		END extract_primer_sequences




def add_biobrick_extensions(): #SUBROUTINE

		final_primers = open("final_primers.fa", 'r').readlines()
		
		print "\tAdding Biobrick Extensions to each primer - these are now RFC 23 compatible:\n"
		
		#Other 5' extensions to use:
		fextwRBS = "CGATCGAGAATTCGCGGCCGCTTCTAGA" + "AGGAGG" + "AACAAU"
		fextwRBSandEnhancer = "GCUCUUUAACAAUUUAUCA" + "GAUCCA" + "AGGAGG" + "AACAAU"
		
		fext = "CGATCGAGAATTCGCGGCCGCTTCTAGA"
		rext = "GCTATGCACTGCAGCGGCCGCTACTAGT"
		
		final_left_primer = fext + final_primers[0][13:]
		final_right_primer = rext + final_primers[1][14:]
		
		print final_left_primer
		print final_right_primer
		
		#END add_biobrick_extensions
		




############# BEGIN PROGRAM ##############

global sequence

if (len(sys.argv) > 2):
	for entry in sys.argv[1:]:
		sequence = entry
		write_primer3_input(sequence)
		run_primer3()
		extract_primer_sequences()
		
elif (len(sys.argv) > 1):
	sequence = sys.argv[1]
	write_primer3_input(sequence)
	run_primer3()
	extract_primer_sequences()
	
else : 	
	# here is where we would say - if command line input has .txt or .fa */
	sequence = 'null'
	write_primer3_input(sequence)





