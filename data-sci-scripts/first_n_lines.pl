#!/usr/bin/perl
# usage:
# ./csv_feature_list.pl abc.txt 4
use Data::Dumper;
binmode STDOUT, ":utf8";

my $text = $ARGV[0];
my $line = $ARGV[1];

open(my $csv, '<:encoding(UTF-8)', $text) or die "Could not open file $text $!";
my $index = 0;
while(my $row = <$csv>){
    $index++;
    print($row);
    if($line eq $index){
        die
    }
}
