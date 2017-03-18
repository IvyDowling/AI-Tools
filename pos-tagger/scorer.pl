#!/usr/bin/perl -w
#Michael Dowling
# This is the scorer for the POS tagger.

binmode STDOUT, ":utf8";

my ($text1, $text2) = @ARGV;

open(my $a, '<:encoding(UTF-8)', $text1) or die "Could not open file $text1 $!";
open(my $b, '<:encoding(UTF-8)', $text2) or die "Could not open file $text2 $!";

my $lineCount = 0;
my %confusion_matrix;
my $total = 0;
my $fp = 0;

while(my $rowa = <$a>){
    $lineCount++;
    my $rowb = <$b>;
    chomp $rowa;
    chomp $rowb;
    $rowa =~ s/[[]//;
    $rowb =~ s/[[]//;
    $rowb =~ s/[]]//;
    $rowa =~ s/[]]//;
    if($rowa=~/\Q$rowb\E/){
        #speed up
        # check if regex eq
        # still have to check total # of correct
        # matches for confusion matrix, but only on 1 string
        my @line_split = ($rowa=~/([^\s]+\/[^\s]+)/g);
        foreach my $k (@line_split){
            my @word_tag_pair = ($k=~/([^\s]+)[\/\b]([^\s]+)/g);
            if(!defined $confusion_matrix{$word_tag_pair[1]}{$word_tag_pair[1]}){
                $confusion_matrix{$word_tag_pair[1]}{$word_tag_pair[1]} = 1;
            } else {
                $confusion_matrix{$word_tag_pair[1]}{$word_tag_pair[1]}++;
            }
            # count total
            $total++;
        }
    } else {
        # whoops
        my @line_splita = ($rowa=~/([^\s]+\/[^\s]+)/g);
        my @line_splitb = ($rowb=~/([^\s]+\/[^\s]+)/g);
        for(my $i=0; $i < scalar @line_splita; $i++){
            chomp $line_splita[$i];
            chomp $line_splitb[$i];
            my @word_tag_paira = ($line_splita[$i]=~/([^\s]+)[\/\b]([^\s]+)/g);
            my @word_tag_pairb = ($line_splitb[$i]=~/([^\s]+)[\/\b]([^\s]+)/g);
            # now, $confusion_matrix{taga}{tagb}++
            if(!defined $confusion_matrix{$word_tag_paira[1]}{$word_tag_pairb[1]}){
                $confusion_matrix{$word_tag_paira[1]}{$word_tag_pairb[1]} = 1;
            } else {
                $confusion_matrix{$word_tag_paira[1]}{$word_tag_pairb[1]}++;
            }
            # did we get this correct?
            if($word_tag_paira[1]=~/\Q$word_tag_pairb[1]\E/){
                # count total
                $total++;
            } else {
                # NOOPE
                # count total
                $total++;
                # count err
                $fp++;
            }
        }
    }
}
print("Total:\t\t$total\n");
my $avg = $total-$fp;
print("CORRECT:\t$avg\n");
print("INCORRECT:\t$fp\n");
$avg = $avg/$total * 100;
print("Average:\t$avg\n");

my @sorted_keys = sort keys %confusion_matrix;
print("\t");
foreach my $print_keys (@sorted_keys){
    if(length $print_keys > 3){
        print("\t$print_keys");
    } else {
        print("\t$print_keys\t");
    }
}
print("\n");
foreach my $ka (@sorted_keys){
    # label
    if(length $ka > 3){
        print("$ka\t");
    } else {
        print("$ka\t\t");
    }
    foreach my $kb (@sorted_keys){
        if(!defined $confusion_matrix{$ka}{$kb}){
            print("0\t\t");
        } else {
            # i like pretty things.
            if(length $confusion_matrix{$ka}{$kb} > 3){
                print("$confusion_matrix{$ka}{$kb}\t");
            } else {
                print("$confusion_matrix{$ka}{$kb}\t\t");
            }
        }
    }
    print("\n");
}
