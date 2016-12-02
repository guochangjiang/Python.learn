#!/usr/bin/perl 
#===============================================================================
#
#         FILE: calculate_pi.pl
#
#        USAGE: ./calculate_pi.pl  
#
#  DESCRIPTION: 根据文件匹配符获取fasta文件列表，并输出到指定文件中
#               加入简并碱基支持(仅支持二倍体)
#
#      OPTIONS: -glob glob.key -out out.keyword
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0
#      CREATED: 2015/5/17 17:06:13
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use utf8;

#use Statistics::Basic qw(:all nofill);
my $glob_key=$ARGV[1];
my $out_key=$ARGV[3];
open OUT, ">$out_key.pi.value.csv";
open AVE, ">$out_key.pi.value.average.csv";
for my $file(glob $glob_key){
    open FILE,"$file";
    print "do file:$file!\n";
    chomp(my @all=<FILE>);
    close FILE;
    $file=~/^(.+)\.fas/;
    my $id=$1;
    my @args = stat ($file);
    my $size = $args[7];
    if($size==0 or $#all<4){
		print OUT "#$id,-\n";
		print AVE "#$id,-\n";
		next;
    }
    
    my %pi=();
    my @pi=();
    my $name='';
    my ($count,$sum,@name);
    for(my $m=0;$m<=$#all;$m+=2){
        $all[$m]=~s/>//;
        push @name,$all[$m];
        for(my $j=$m+2;$j<=$#all;$j+=2){
            my $e_length=0;    # 两条序列重叠部分碱基总数
            my $d_length=0;    # 两条序列重叠部分不同碱基总数
            my $name2=substr($all[$j],1,);
            $all[$m+1]=uc $all[$m+1];
            for(my $i=0;$i<length($all[$m+1]);$i++){
                $all[$j+1]=uc $all[$j+1];
                my $base1=substr($all[$m+1],$i,1);
                my $base2=substr($all[$j+1],$i,1);
                if($base1=~/[ATCGMRWSYKVHDB]/ && $base2=~/[ATCGMRWSYKVHDB]/){
                    $e_length++;
                    if($base1=~/[ATCG]/ && $base2=~/[ATCG]/ && $base1 ne $base2){
                        $d_length++;
                    }
                    if($base1=~/[ATCG]/ && $base2=~/[MRWSYKVHDB]/){
                        @bases = Get_Degenerate_Base($base2);
                        my $same = 0;
                        for(my $b=0;$b<=$#bases;$b++){
                            if($bases[$b] eq $base1){$same++;}
                        }
                        $d_length += ($#bases+1-$same)/($#bases+1);
                    }
                    if($base2=~/[ATCG]/ && $base1=~/[MRWSYKVHDB]/){
                        @bases = Get_Degenerate_Base($base1);
                        my $same = 0;
                        for(my $b=0;$b<=$#bases;$b++){
                            if($bases[$b] eq $base2){$same++;}
                        }
                        $d_length += ($#bases+1-$same)/($#bases+1);
                    }
                    if($base1=~/[MRWSYKVHDB]/ && $base2=~/[MRWSYKVHDB]/){
                        @bases1 = Get_Degenerate_Base($base1);
                        @bases2 = Get_Degenerate_Base($base2);
                        $total_num = 0;
                        $diff_num = 0;
                        for my $b1 (@bases1){
                            for my $b2 (@bases2){
                                $total_num++;
                                if($b1 ne $b2) {$diff_num++;}
                            }
                        }
                        if($diff_num == $total_num) {$d_length++;}
                        else{$d_length += 0.5}
                    }
                }
            }
            my $pi=$d_length/$e_length;
            $pi=(-3/4)*log(1-(4/3)*$pi);
            push (@pi,$pi);
            $sum+=$pi;
            $count++;
            #print "        length:$e_length!\n"
        }
       
        
    }
    $file=~s/.fas//;
    my $ave=$sum /$count;
    print OUT "#$id,average=$ave\n";
    print AVE "#$id,$ave\n";
    print OUT "$_," foreach @name;
    print OUT"\n";
    my $bs=0;
    for ($bs=0;$bs<$#name;$bs++){
        print OUT "$name[$bs]";
        my $sheep="," x($bs+1);
        print OUT "$sheep";
        for (my $i=0;$i<=$#name-1-$bs;$i++){
            print OUT "$pi[0],";
            shift @pi;
        }
        print OUT"\n";
    #my $ave=$sum /$count;
    #my @line=split/,/,$name;
    #print OUT "$file,average,";
    ##printf OUT "%6f\n";
    #print OUT ",$name\n";
    #for(my $i=0;$i<=$#line;$i++){
    #    for(my $j=0;$j<=$#line;$j++){
    #        #print "$line[$j]\n";
    #        if(defined $pi{$line[$i]}{$line[$j]}){
    #            printf OUT "%6f,",$pi{$line[$i]}{$line[$j]};
    #        }else{
    #            print OUT ",";
    #        }
    #    }
    #    print OUT "\n";
    }
    print OUT "\n";
}

sub  Get_Degenerate_Base{
	base = $_[0]
	if(base eq 'M'){return ('A', 'C');}
	elsif(base eq 'R'){return ('A', 'G');}
	elsif(base eq 'W'){return ('A', 'T');}
	elsif(base eq 'S'){return ('C', 'G');}
	elsif(base eq 'Y'){return ('C', 'T');}
	elsif(base eq 'K'){return ('T', 'G');}
	elsif(base eq 'V'){return ('A', 'C', 'G');}
	elsif(base eq 'H'){return ('A', 'C', 'T');}
	elsif(base eq 'D'){return ('A', 'T', 'G');}
	elsif(base eq 'B'){return ('T', 'C', 'G');}
	else{print("Error base: $base")}
}