#!/usr/bin/perl
# usage:
# ./csv_feature_list.pl abc.txt 4
use Data::Dumper;
binmode STDOUT, ":utf8";

my $text = $ARGV[0];
my $line = $ARGV[1];

open(my $csv, '<:encoding(UTF-8)', $text) or die "Could not open file $text $!";
my $index = 0;
while(my $firstline = <$csv>){
    $index++;
    if($line eq $index){
        my @commas = split /,/, $firstline;
        my $TABLE_LENGTH = $#commas;
        print Dumper(\@commas);
        die
    }
}
