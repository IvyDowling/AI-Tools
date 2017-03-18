#!/usr/bin/perl -w
#Michael Dowling
# This tool is a Part of Speech tagger that is trained on
# a dataset then uses its hash of "most likely tag" given
# the word to calssify an unknown set.
#
# The process involves a read-in loop, which blindly loads
# a hash with every instance of a word->tag->#oftimes it's
# been seen. This hash is then taken and is used to make
# a trimmed hash, where we only have word ->most-common-tag
#
# I'm using Data::Dumper to print out my hashes
# My rules that I implemented first are:
# If we dont know what the word is
#   1. if \d, CD
#   2. if it ends in 's', NNS
#   3. if it starts with a capital, NNP
#   4. otherwise NN
#
# Right now, acc = 88%, and the largest issue is
# JJ we're classifying as NN. 881 of ~3000 JJs
# To fix this issue, I first approached some of the mis-classified NNs,
# by using Upper case to pick out more Proper Nouns
# This, however lowers the acc = 86% because we're picking up every
# sentence beginning, so perhaps we could add in a "new_sentence"
# variable to see how much improvement we get.
# This only got me up to acc = 88.7%, which is an increase I'll take
# because this is a more logical way to do general Noun mapping 
use Data::Dumper;
binmode STDOUT, ":utf8";

# will help with beginning our sentences later

my ($train, $test) = @ARGV;

my %training_tokens;
open(my $training, '<:encoding(UTF-8)', $train) or die "Could not open file $train $!";
while(my $row = <$training>){
    chomp $row;
    # training text in format:
    #   [ the/DT lungs/NNS ]
    #      - OR -
    #   ,/, with/IN
    # so we remove phrasal boundries
    $row =~ s/[[]]//;
    # split -> [word]/[words]
    # adding \b on the edges screws with ./. and ,/,
    my @line_split = ($row=~/([^\s]+\/[^\s]+)/g);
    foreach $match (@line_split){
        chomp $match;
        $match = lc($match);
        # break into two keys, words[0] tag[1]
        my @word_tag_pair = ($match=~/([^\s]+)[\/\b]([^\s]+)/g);
        # now, training_tokens{word}{tag}++
        if(!defined $training_tokens{$word_tag_pair[0]}{$word_tag_pair[1]}){
            $training_tokens{$word_tag_pair[0]}{$word_tag_pair[1]} = 1;
        } else {
            $training_tokens{$word_tag_pair[0]}{$word_tag_pair[1]}++;
        }
    }
}
#print Dumper \%training_tokens;
# now we've loaded the entire trainging set,
# time to reduce our hash into the most-likely tags.
# instead of just deleting elements, I'll
# make a new hash where only word -> tag
my %model;
foreach $k (keys %training_tokens){
    my $count = 0;
    my $tag;
    foreach $t (keys $training_tokens{$k}){
        if($training_tokens{$k}{$t} > $count){
            $count = $training_tokens{$k}{$t};
            $tag = $t;
        }
    }
    $model{$k} = $tag;
}
#print Dumper \%model;
open(my $testing, '<:encoding(UTF-8)', $test) or die "Could not open file $test $!";
# lets see if this helps with our NNP classifying
my $sentence_start;
while(my $row = <$testing>){
        chomp $row;
        my @line_split = ($row=~/([^\s]+)/g);
        foreach $match (@line_split){
            chomp $match;
            $lcmatch = lc($match);
            # CLASSIFY!
            if(!$model{$lcmatch}){
                # if we don't see any value relating to this word
                if($match=~/[[]/){
                    #brackets must be skipped
                    print("$match ");
                } elsif($match=~/[]]/){
                    #brackets must be skipped
                    print("$match ");
                } elsif ($match=~/[\d]+/) {
                    #If it contains digits, CD
                    print("$match/CD ")
                } elsif ($match=~/\b[A-Z][\w]+/) {
                    # capital letter might be NNP
                    print("$match/NNP ")
                } elsif($match=~/[\w+]s]/){
                    #if it ends in 's' lets take a chance on calling it plural
                    print("$match/NNS ")
                } else {
                    #NN
                    print("$match/NN ")
                }
            } else {
                # we have a most-common-tag for this word
                if ($match=~/\b[A-Z][\w]+/) {
                    if(defined $sentence_start){
                        $t = uc $model{$lcmatch};
                        print("$match/$t ");
                    } else {
                        # capital letter might be NNP
                        print("$match/NNP ")
                    }
                } else {
                    $t = uc $model{$lcmatch};
                    print("$match/$t ");
                }
            }
        }
        #check at the bottom for next round
        # all of the sentences end on a \n
        # get last line_split element
        if($line_split[$#line_split]=~/[.?!]/){
            $sentence_start = $line_split[$#line_split];
        } else {
            undef $sentence_start;
        }
        print("\n")
}
