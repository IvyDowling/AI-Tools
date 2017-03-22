#!/usr/bin/perl
binmode STDOUT, ":utf8";

my $text = $ARGV[0];

open(my $csv, '<:encoding(UTF-8)', $text) or die "Could not open file $text $!";
my $firstline = <$csv>;
my @commas = split /,/, $firstline;
my $TABLE_LENGTH = $#commas;
print("$text has $TABLE_LENGTH features\n");
