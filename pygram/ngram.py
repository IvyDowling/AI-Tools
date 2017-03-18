import sys
import re
import json
import random as rand


def make_ngram(input_list, n):
    # amazing line, found, online > list(zip(*[input_list[i:] for i in range(n)]))
    # but I'd ratheruse a python dictionary here,
    # http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
    gram = list(zip(*[input_list[i:] for i in range(n)]))
    # add on a base frequency,on the list
    # start at 0 because we'll match ourselves in this alg
    gram = [list(i) for i in gram]
    input_dict = {}
    for g in gram:
        # does this value exist in our dict
        leaf_val = find_dict_leaf(input_dict, g)
        #print(leaf_val)
        if  leaf_val != None:
            # this gram has been seen before
            input_dict = merge_dicts(input_dict, list_to_dict(g, leaf_val + 1))
        else:
            # new gram
            input_dict = merge_dicts(input_dict, list_to_dict(g, 1))

    #print(gram)
    print(json.dumps(input_dict, indent=3))
    return input_dict


def list_to_dict(gram_list, v):
    if(len(gram_list) == 1):
        return {gram_list[0] : v}
    else:
        return {gram_list[0] : list_to_dict(gram_list[1:], v)}


def find_dict_leaf(d, key_list):
    if d == None:
        return None
    if len(key_list) == 1:
        if d.get(key_list[0]) is None:
            return None
        else:
            return d.get(key_list[0])
    else:
        return find_dict_leaf(d.get(key_list[0]), key_list[1:])


def merge_dicts(orig_dict, add_dict):
    out = orig_dict.copy()
    for k, v in add_dict.items():
        out.update({k:v})

    return out


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


def markov(tokens, n):
    print("Starting Markov")
    phrase = []
    # starting point is a word that followed a '.','?','!'
    punct = rand.randint(0,3);
    token_keys = list(tokens["."].keys())
    start = "."
    print(start)
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
        print("try: ngram.py [gram-size] [number of output sentences] [file.txt]")
