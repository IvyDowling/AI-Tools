#!/usr/bin/perl
binmode STDOUT, ":utf8";

my $text = $ARGV[0];

open(my $csv, '<:encoding(UTF-8)', $text) or die "Could not open file $text $!";

while(my $row = <$csv>){
    $row =~ s/['"]//g;
    $row =~ s/[\n]//g;
    print($row);
    # dont forget the line break that we deleted...
    print("\n");
}
