#!/usr/bin/env python
import sys
from Bio import SeqIO

def run_primer3(): 
        print "Running Primer3 for %i...............\n\n" %id
        primer = open('primer3_core')
        primer.append('primer3/primer3_input') 
        
                #BEGIN TO LOOSEN THRESHOLDS IF PRIMER3 DOESN'T FIND ANY PRIMERS - ADD PARAMETERS OTHER THAN Tm

        while primer[primer.len() - 1] == 0:
                        print "\nReworking primer3 parameters\n\n"
                
                        primer3_input = open("/primer3/primer3_input")
                        
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
                        open ("/primer3/primer3_input")
                        print primer3_input
    
                #IF PRIMERS ARE FOUND, PRIMER3 OUTPUT IS APPENDED TO PRIMER3_OUTPUT
                        print "PRIMER3 OUTPUT FOR %i: \n\n" % id
                        print "\n\nPRIMER3 OUTPUT for %i: \n\n" % id
                        print primer
                        print PRIMER3_OUTPUT + primer
        
        
                        close("/primer3/primer3_input")
                        #END run_primer3


def extract_primer_sequences(): #SUBROUTINE
        primer3_output = open("/primer3/primer3_output.txt")
        
        primer3_sequences = open("final_primers1.fa")
        
        #map(line, primer3_output)
                #chomp line
                
        if line == primer3_output:
                id = line
                id = primer3_output
                
        if line == primer_left_0_sequence:
                left = line
                left = primer_left_0_sequence
                
        if line == primer_right_0_sequence:
                right = line
                right = primer_right_0_sequence
                
        if line == primer_left_0_problems:
                left_problems = line
                left_problems = primer_left_0_problems
                
        if line == primer_right_0_problems:
                right_problems = line
                right_problems = primer_right_0_problems
                
        if left == true and right == true and id == true:
                print "Left_Primer_0_for: %i\n %l \n" %(id, left)
                print "Right_primer_0_for: %i\n %r \n" %(id, right)
                        
        if left_problems == true or right_problems == true:
                print "Made the best primers possible, but there might still be some issues:\n"
        if left_problems == true:
                print "Potentional problems with the left primer: %l" %left_problems
        if right_problems == true:
                print "Potential problems with the right primer: %r" %right_problems
                        
        left_primer = left
        right_primer = right
                        
        left = false
        right = false
        id = false
        left_problems = false
        right_problems = false

        close("final_primers1.fa")
        close ("primer3/primer3_output.txt")
        #END extract_primer_sequences

def add_biobrick_extensions(): #SUBROUTINE

        print "\n\nAdding Biobrick Extensions to each primer - these are now RFC 23 compatible:\n\n"
        
        fext = "CGATCGAGAATTCGCGGCCGCTTCTAGA"
        rext = "GCTATGCACTGCAGCGGCCGCTACTAGT"
        
        final_left_primer = fext + left_primer
        final_right_primer = rext + right_primer

        #END add_biobrick_extensions

def define_seq_dict():
	seq_dict = [(">recG", "agctagctagcatcgatcagactagctacacttacgactacgactacgtactcagatcagtacgactacgactacgcatcgcatcatacgcatacgactacacactacgatcatctatcatcagtcgactacgtc")]
		

def cloning_primers_from_fafile(file):    
#         print "Loading fasta file:"
#         print input_fasta_file 
# 
#         input_fasta_file(format) = 'Fasta'
#         file = input_fasta_file
#         
#         while current_seq == infile*(next_seq()):
#                 print "OK, we're designing primers for this sequence:\n"
#         print current_seq*id
#         print "\n\n"
#         gene = current_seq*id
    	
    	define_seq_dict()
    	sequence = seq_dict[">recG"]
    
        #FORMAT SEQUENCE TO TURN ANYTHING NOT A, T, G, OR C INTO N
#       sequence = current_seq*seq
        sequence = sequence.replace(("S", "N")("Y", "N")("R", "N")("W", "N")("K", "N")("M", "N")("s", "N")("y", "N")("r", "N")("w", "N")("k", "N")("m", "N")) #replaces syrwkm with n NOTE: TRY TO FIND MORE EFFICIENT REPLACEMENT METHOD
    
        #OPENS TEXT FILE AND PUTS IT INTO ARRAY
        primer3file = open('/primer3/cloning_primer3_options.txt')      
        primer3options = primer3file
    
        #PRINTS PRIMER3_OUTPUT.txt
        open('/primer3/PRIMER3_OUTPUT.txt')
        print('/primer3/PRIMER3_OUTPUT.txt')
    
        #CONSTRUCT PRIMER3 OPTIONS FILE, RUN PRIMER3 AND SAVE FILE TO PRIMER3_OUTPUT
        product_size = len(sequence)
        print "Product size here is: %x" % product_size
                
        end_base = product_size - 1
        sequence_template = "SEQUENCE_TEMPLATE = %x \n" % sequence
        target = "SEQUENCE_INCLUDED_REGION = 0, %x \n" % end_base
        print "Writing primer3 input file for %x \n\n" % gene 
    
        output = open('/primer3/primer3_input')
        output.write(sequence_template)
        output.write(target)
        output.write(primer3options[0:])    
    
        #PRINT FINAL PRIMERS TO FILE
        final_output = open("final_primers1.fa")
        
        print "%f for %g \t" % (final_output, gene) #override final_output with gene , print file
        print "%f %g \n" % (final_output, final_left_primer) # print new file with override gene
        print "%f Rev %g \t" % (final_output, gene) 
        print "%f %g \n" % (final_output, final_right_primer)
        
        print "Forward Biobricking Primer for %g :\n" % gene 
        print "%g \n" % final_left_primer
        print "Reverse Biobricking Primer for %g :\n" % gene 
        print "%g \n" % final_right_primer
    
        close('final_primers1.fa')
        close('/primer3/primer3_input')
        close('/primer3/cloning_primer3_options.txt') #closes file at end of subroutine

        print "\n\nExiting..............\n\n"
    #END cloning_primers_from_fafile

command_line_input = raw_input("Please enter the file with the genetic sequence you would like to provide primers for: ")

if /*defined sys.argv[1] as .txt, .fa, .fasta */ 

if ".txt" or ".fa" or ".fasta" in command_line_input:
        
        print "LINE 1-177 COMPLETED"
        
        input_fasta_file = command_line_input
        cloning_primers_from_fafile(input_fasta_file)
else:
        print "\n\nNo file identified, unable to run program." 
