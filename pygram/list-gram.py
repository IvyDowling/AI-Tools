import sys
import re
import random as rand


def find_ngrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))


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

    tokens = find_ngrams(huge_list, n)
    for i in range(m):
        out = ""
        for w in markov(tokens, n):
            out += str(w) + " "
        print(out)


def markov(tokens, n):
    phrase = []
    # starting point
    start = tokens[rand.randint(0, len(tokens))]
    while True:
        if re.match('\W+', str(start)):
            phrase.append(start)
            break
        else:
            start = tokens[rand.randint(0, len(tokens))]
    while True:
        # take the last n-1 words in the
        # phrase and match them to another
        window = phrase[-(n - 1):]
        swap = window
        # this match limits the list to grams that
        # have the same first word that as our window
        for match in [gram for gram in tokens if gram[0] == window[0]]:
            m = list(match)
            if m[:-1] == window:
                phrase.append(m[n - 1])
                window = phrase[-(n - 1):]
            if str(m[n - 1]) == "." or str(m[n - 1]) == "?" or str(m[n - 1]) == "!":
                return list(phrase)
        if swap == window:
            # we're stuck
            phrase.append(".")
            return list(phrase)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        run(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
    else:
        print("what csv file?")
