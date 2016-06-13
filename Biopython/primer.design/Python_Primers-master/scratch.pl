	    #PRINT FINAL PRIMERS TO FILE
        final_output = open("final_primers1.fa")
        
        print "%f For %g \t" % (final_output, gene) #override final_output with gene , print file
        print "%f %g \n" % (final_output, final_left_primer) # print new file with override gene
        print "%f Rev %g \t" % (final_output, gene) 
        print "%f %g \n" % (final_output, final_right_primer)
        
        print "Forward Biobricking Primer for %g :\n" % gene 
        print "%g \n" % final_left_primer
        print "Reverse Biobricking Primer for %g :\n" % gene 
        print "%g \n" % final_right_primer
        	
        close('final_primers1.fa')
        close('./primer3/primer3_input')
        close('./primer3/cloning_primer3_options.txt') #closes file at end of subroutine

        print "\n\nExiting..............\n\n"


