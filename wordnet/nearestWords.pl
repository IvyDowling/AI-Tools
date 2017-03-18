#!/usr/bin/perl

# This shows 4 comparisons of Similarity on the WerdNet

use WordNet::QueryData;
use WordNet::Similarity::lesk;
use WordNet::Similarity::wup;
use WordNet::Similarity::vector;
use WordNet::Similarity::res;
my $qd = WordNet::QueryData->new();
my $wnlesk = WordNet::Similarity::lesk->new($qd);
my $wnwup = WordNet::Similarity::wup->new($qd);
my $wnvector = WordNet::Similarity::vector->new($qd);
my $wnres = WordNet::Similarity::res->new($qd);
my $a = <STDIN>; chomp $a;
my $b = <STDIN>; chomp $b;
my $leskscore = $wnlesk->getRelatedness("$a#n#1", "$b#n#1");
my $wupscore = $wnwup->getRelatedness("$a#n#1", "$b#n#1");
my $vectorscore = $wnvector->getRelatedness("$a#n#1", "$b#n#1");
my $resscore = $wnres->getRelatedness("$a#n#1", "$b#n#1");
print "lesk = $leskscore\n";
print "wup = $wupscore\n";
print "vector = $vectorscore\n";
print "res = $resscore\n";
