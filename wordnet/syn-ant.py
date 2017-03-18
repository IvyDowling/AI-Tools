from nltk.corpus import wordnet

# This program was for a nlp robot
# the intention was to simply use
# synonyms or antonyms to add to the Turing
# illlluuuusssiiioooon~~~

def run(token):
    synonyms = []
    antonyms = []
    for syn in wordnet.synsets(token):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    print(set(synonyms))
    print(set(antonyms))

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        tk = sys.argv[1].lower()
        run(tk)
    else:
        print("what values are you looking for?")
