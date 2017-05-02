#!/usr/bin/perl
# usage:
# ./line_killer.pl abc.txt 4
# deletes line 4
use Data::Dumper;
binmode STDOUT, ":utf8";

my $text = $ARGV[0];
my $line = $ARGV[1];

open(my $csv, '<:encoding(UTF-8)', $text) or die "Could not open file $text $!";
my $index = 0;
while(my $row = <$csv>){
    $index++;
    if($line eq $index){
        # NOPE
    } else {
        print($row)
    }
}
