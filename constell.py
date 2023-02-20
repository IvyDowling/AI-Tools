#!/usr/bin/python
import curses, random

import math
import random
#import numpy as np

#
# Arrays, used for translation PrimeRepresentation -> ASCII: 1 Char 
#
P = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491] #, 499, 503, 509, 521, 523 ]
AT = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
A = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/']
#t = np.array([P,AT], np.int32)
#
# Programatic Setup
# len(A) = len(P)
#
globalLen = len(A)
globalAxis = math.floor(globalLen/2)

def minPLength(x):
    # as we change our scope, the values we must encode also change relatively
    # optical loss must be avoided, by making sure the small lens is never too
    # small to operate: ie minLength
    # All even base ten numbers are of the form 2n where n is a non-even number
    #   n could be prime, it might be just odd.
    #   if n is odd, non-prime, it is divisible by another prime, not 2
    #       using mod fn, we can find the prime representation by using our prime list
    #       - I have a greedy solution, we only want min(max-prime),
    #       so lets just count backwards from n until we find a prime? then we have a
    #       remainder, 2, and maxPrime, recurse for remainder? Could be a prime too, check!
    #
    #   we could do a lot of shortcuts with a conversion IndexToPrime, 1st, 2nd, 3rd...******
    if(x % 2 == 0):
        return 2
    # we have an odd number
    n = x - 1
    # len min 3: (1, 2, n)
    returnLength = 3
    half = int(n / 2)
    # now, greedy minimizer
    looping = True
    while (looping):
        e = list(filter(lambda n: half in n, P))
        print(e)
        if(e):
            # winner, we know the maxPrime factor 
            P.index(half)
            looping = False
            if(returnLength == 3):
                return 3
        else:
            # this will be assigned a bunch of times,
            # but this is the first time we KNOW it will be min4
            returnLength = 4
            half = half - 1
    # now we only have to sort out the remainder.
    # this might be trivial, like an early prime number
    rem = int(n/2) - half
    if(P.contains(rem)):
        return 4
    else:
        # let the alg handle it
        returnLength = returnLength + minPLength(rem)
    return returnLength


def maxPrimeIndex(x):
    if (x in P):
        return P.index(x)
    # simplicity
    return P.index(maxPFactor(x))
        

def maxPFactor(x):
    half = int(x / 2)
    # now, greedy minimizer
    looping = True
    while (looping):
        if(half in P):
            # winner, we know the maxPrime factor 
            return half
        else:
            half = half - 1


def markov(x):
    # markov chains work by creating a possible list based on an corpus input
    # in text, this is represented by the possibility of one word to follow another
    # "I will go to the...": 3% basement, 15% store 16% show ....     
    #
    # Markov chains actually turn the input into a function,
    # where input (n1 -> n2), (n1 -> n3) ... probabilistically
    # 
    # If i were to represent a 'Prime Incarnation' like this,
    # there would be a min-length: see minPLength(), max length: x(0s).
    # To get the rest, we would need to use markovs to give us
    # Possibile Views... If you want to say it that way
    # 
    # Pick a number in the prime set for input x
    #
    # Whats the max factor? Thats how we make our fn
    if(x in P):
        # we're prime...
        return [x]
    m = maxPFactor(x)
    iM = P.index(m)
    # markovs are great, lets put this baby together
    # we should be able to actually shrink our lens
    # to minimize travesrsals
    # there are many ways to begin a markov, random works ok
    a = random.randint(0, iM + 1)
    primeIncar = [P[a]]
    looping = True
    while (looping):
        b = markovNext(x, primeIncar)
        primeIncar.append(b)
        if (sum(primeIncar) == x):   
            looping = False
            return primeIncar
        if (sum(primeIncar) > x):
            # lazy helper, do I need this?? too big
            primeIncar = primeIncar[:-1]
        

def markovNext(x, ps):
    # x is goal, ps is a list of primes at least length 1
    # x - sum of this list gives us our remainder to work with
    rem = x - sum(ps)
    if(rem > 0):
        if(rem == 1):
            return 1
        if(rem == 2):
            return 2
        if(rem == 3):
            return 3
        m = maxPFactor(rem)
        iM = P.index(m)
        return P[random.randint(0, iM + 1)]
        
def transform(ps):
    # ps is a list of primes
    asciiPrimes = []
    for p in ps:
        asciiPrimes.append(A[P.index(p)])
    return asciiPrimes

def prettyList(l):
    res = ''
    for i in l:
        res += i
    return res


############################################
mTarget = 901
############################################


screen  = curses.initscr()
width   = screen.getmaxyx()[1]
height  = screen.getmaxyx()[0]
size    = width*height
b       = []

curses.curs_set(0)
curses.start_color()
for i in range(1, len(P)):
    curses.init_pair(i, len(P)-i, i)

screen.clear

outputs = []
for r in range(0,size):
    # population
    pop = 200
    smpl = 0.15 
    if(random.randrange(0, pop) > int(pop*smpl)):
        outputs.append(' ') 
    else:
        mT = markov(mTarget)
        p = transform(mT)
        outputs.append(prettyList(p))


for i in range(size+width+1):
    b.append(0)

tick = 0
while 1:
    for i in range(size):
        if (outputs[i] == ' '):
            b[i] = ' '
            color = 0
        else:
            b[i]= outputs[i % len(outputs)][tick % len(outputs[i])]
            color= ord(b[i]) % len(P)
        if(i < size-1):
            screen.addstr(int(i/width), i%width, b[i], curses.color_pair(color))

    tick = tick + 1
    screen.refresh()
    screen.timeout(200)
    if (screen.getch() != -1 or tick > 9999):
        break

curses.endwin()
