#!/usr/bin/env perl 
#===============================================================================
#
#         FILE: calculate.tajimaD.aln.fas.pl
#
#        USAGE: ./calculate.tajimaD.aln.fas.pl  
#
#  DESCRIPTION: 根据已排序的fas文件计算其Tajama's D，忽略非ATGC位点
#
#      OPTIONS: -in xx.aln.fasta
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 2.0
#      CREATED: 2015/6/22 14:49:18
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use utf8;

my $in_file=$ARGV[1];

open IN,"$in_file" or die;
my @name;
my %sequence;
my $name;

while(<IN>){
	chomp;
	next unless $_;
	if(/^>/){
		$name=$_;
		$name=~s/^>//;
		push @name,$name;
	}
	else{$sequence{$name}.=uc $_;}
}
close IN;

my $m=$#name+1;
my $n=length $sequence{$name[0]};

my $a1;
my $a2;
for(my $i=1;$i<$m;$i++){
	$a1+=1/$i;
	$a2+=1/($i*$i);
}
my $b1=($m+1)/($m-1)/3;
my $b2=2*($m*$m+$m+3)/9/$m/($m-1);
my $c1=$b1-1/$a1;
my $c2=$b2-($m+2)/($a1*$m)+$a2/($a1*$a1);
my $e1=$c1/$a1;
my $e2=$c2/($a1*$a1+$a2);

my $S;
for(my $i=1;$i<=$n;$i++){
	my @base=();
	foreach my $key (sort keys %sequence){
		push @base,substr($sequence{$key},$i-1,1);
	}
	my $flag=&IsSame(@base);
	$S+=$flag;
}

my $pi;
my $count;
my $pair;

for(my $i=0;$i<$#name;$i++){
	for(my $j=$i+1;$j<=$#name;$j++){
		$pair++;
		for(my $k=1;$k<=$n;$k++){
			my $base1=substr($sequence{$name[$i]},$k-1,1);
			my $base2=substr($sequence{$name[$j]},$k-1,1);
			$count++ if $base1 ne $base2 && $base1=~/[ATGC]/ && $base2=~/[ATGC]/;
		}
	}
}
$pi=$count/$pair;
my $tajimaD=($pi-$S/$a1)/sqrt($e1*$S+$e2*$S*($S-1));
print "The tajima's D is: $tajimaD\n";
print "m=$m\nlength=$n\npi:$pi\nS=$S\n";
#print "a1=$a1\ta2=$a2\tb1=$b1\tb2=$b2\n";
#print "c1=$c1\tc2=$c2\te1=$e1\te2=$e2\n";



sub IsSame{
	my @str=@_;
	my $str0;
	foreach my $str (@str){
		$str0=$str[0] if $str[0]=~/[ATGC]/;
	}
	
	my $flag=0;
	foreach my $str (@str){
		if($str0 ne $str  && $str=~/[ATGC]/){$flag=1;last;}
	}
	return $flag;
}