#!/usr/bin/perl
# usage:
# ./csv_feature_list.pl abc.txt 4
use Data::Dumper;
binmode STDOUT, ":utf8";

my $text = $ARGV[0];
my $feature = $ARGV[1];

open(my $csv, '<:encoding(UTF-8)', $text) or die "Could not open file $text $!";
my $index = -1;
my @firstline = split /,/, <$csv>;
( $index ) = grep { $firstline[$_] =~ /$feature/ } 0..$#firstline;
if (!$feature eq $firstline[$index]){
    die "No feature $feature found in csv $text.\n '$feature' =/= '$firstline[$index]'\n"
}
my $data_count = 0;
my $total = 0;
while(my $row = <$csv>){
    my @split = split /,/, $row;
    if($split[$index] != "?"){
        $data_count++;
    }
    $total++;
}
my $avg = $data_count / $total * 100;
print("Found $data_count / $total = $avg data points were not '?'\n");
