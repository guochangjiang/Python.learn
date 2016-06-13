#!/usr/bin/env perl 
#===============================================================================
#
#         FILE: calculate.pi.between.2.fasta.pl
#
#        USAGE: ./calculate.pi.between.2.fasta.pl  
#
#  DESCRIPTION: 根据统一比对fasta文件按group分拆(jap.ind)的fasta文件计算二者之间的group间的平均pi值(按照指定顺序)
#
#      OPTIONS: -glob globkey -key1 key1 -key2 key2 -out outkey
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0
#      CREATED: 2015/5/17 22:01:35
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use utf8;

my $glob_key=$ARGV[1];
my $key1=$ARGV[3];
my $key2=$ARGV[5];
my $loci_order=$ARGV[7];
my $out_key=$ARGV[9];
open OUT,">$out_key.average.pi.csv";

open ORD,"$loci_order" or die;
my @order;
while(<ORD>){
	chomp;
	push @order,"$_.$glob_key";
}
close ORD;

my @files=@order;
foreach my $file (@files){
	my $file1=$file;
	my $file2=$file;
	$file2=~s/$key1/$key2/;
	my @args_1 = stat ($file1);
	my @args_2=stat ($file2);
	my $size_1=$args_1[7];
    my $size_2 = $args_2[7];
	print "$file1---------$file2\n";
	$file=~/(LOC_Os\d+g\d+\.\d+)/;
	my $locus=$1;
	if($size_1==0 or $size_2==0){print OUT "#$locus\t-\n";next;}
	my $sum=0;
	my $count=0;
	open F1,"<$file1" or die;
	open F2,"<$file2" or die;
	chomp (my @array1=<F1>);
	chomp (my @array2=<F2>);
	close F1;
	close F2;
	my $i=0;
	while($i<$#array1){
		my $seq1=uc $array1[$i+1];
		my $j=0;
		while($j<$#array2){
			my $e_length=0;
			my $d_length=0;
			my $seq2=uc $array2[$j+1];
			for(my $k=0;$k<length ($seq1);$k++){
				my $base1=substr($seq1,$k,1);
				my $base2=substr($seq2,$k,1);
				if($base1=~/[ATGC]/ && $base2=~/[ATGC]/){
					$e_length++;
					if($base1 ne $base2) {$d_length++;}
				}
			}
			my $pi=$d_length/$e_length;
			$pi=(-3/4)*log(1-(4/3)*$pi);
			$sum+=$pi;
			$count++;
			#print "$count\n";
			$j+=2;
		}
		$i+=2;
	}
	my $ave=$sum/$count;
	print OUT "#$locus,$ave\n";	
}
close OUT;
