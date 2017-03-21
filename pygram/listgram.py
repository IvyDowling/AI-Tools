import sys
import re
import json
import random as rand


def run(n, m, *argv):
    huge_list = []
    for f in argv:
        this_file = open(f)
        for ln in this_file:
            # \n
            ln = ln.strip()
            if ln is not "":
                # splits on words
                words = re.split('([\w\'\-]+)', ln)
                # delete spaces and empty strings
                words = [w for w in words
                         if (w is not " " and
                             w is not "" and
                             w is not '"')]
                for w in words:
                    huge_list.append(w)

    tokens = make_ngram(huge_list, n)
    for i in range(m):
        out = ""
        for w in markov(tokens, n):
            out += str(w) + " "
        print(out)


def make_ngram(input_list, n):
    # amazing line, found, online > list(zip(*[input_list[i:] for i in range(n)]))
    # http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
    gram = list(zip(*[input_list[i:] for i in range(n)]))
    # add on a base frequency,on the list
    # start at 0 because we'll match ourselves in this alg
    gram = [list(i) for i in gram]

    # print(gram)
    # print(json.dumps(input_dict, indent=3))
    return gram


def markov(tokens, n):
    # Start generating
    # tokens is an n-gram
    # we want this to be shuffled before start
    rand.shuffle(tokens)
    phrase = []
    # starting point is a word that followed a '.','?','!'
    punct = rand.randint(0, 3);
    start = "."
    if punct == 1:
        start = "?"
    if punct == 2:
        start = "!"
    # get first n-length phrase to start
    for gram in tokens:
        if gram[0] == start:
            phrase = list(gram)[1:]
            if "." in phrase or "?" in phrase or "!" in phrase:
                return list(phrase)
            break

    while True:
        # take the last n-1 words in the
        # phrase and match them to another
        # - on first run, takes whole phrase
        window = phrase[-(n - 1):]
        swap = window.copy()
        # this match limits the list to grams that
        # have the same first word that as our window
        for match in [gram for gram in tokens if gram[0] == window[0]]:
            m = list(match)
            if m[:-1] == window:
                phrase.append(m[n - 1])
                window = phrase[-(n - 1):]
                rand.shuffle(tokens)
            # If we've picked up a punctuation mark
            # lets break here
            if phrase[-1] is "?" or phrase[-1] is "!" or phrase[-1] is ".":
                return list(phrase)
        if swap == window:
            # we're stuck
            # best course of action here is to redo
            phrase = []
            punct = rand.randint(0, 3);
            start = "."
            if punct == 1:
                start = "?"
            if punct == 2:
                start = "!"
            for gram in tokens:
                if gram[0] == start:
                    phrase = list(gram)[1:]
                    if "." in phrase or "?" in phrase or "!" in phrase:
                        return list(phrase)
                    break


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        run(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
    else:
        print("try: ngram.py [gram-size] [number of output sentences] [file.txt]")
