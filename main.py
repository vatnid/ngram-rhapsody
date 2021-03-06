#!/usr/bin/env python3

from collections import defaultdict
import math
import numpy as np
import sys
from datetime import datetime


def train(source, target):

    tri_counts = defaultdict(int)
    tri_probs = defaultdict(int)

    bi_counts = defaultdict(int)
    uni_counts = defaultdict(int)

    with open(source) as f:
        for line in f:
            line = "##" + line.strip().lower() + "##"
            # trigrams
            for j in range(len(line)-2):
                trigram = line[j:j+3]
                tri_counts[trigram] += 1
            # bigrams
            for j in range(len(line)-1):
                bigram = line[j:j+2]
                bi_counts[bigram] += 1
            # unigrams
            for j in range(len(line)):
                unigram = line[j:j+1]
                uni_counts[unigram] += 1

    for item in tri_counts:
        tri_probs[item] = tri_counts[item] / sum([tri_counts[x] for x in tri_counts if x[0:2] == item[0:2]])
        print(item, tri_probs[item])

    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")
    with open((f"{target}_{date_time}"), "w") as f:
        for item in tri_probs:
            f.write(f"{item}\t{tri_probs[item]}\n")

    tri_probs = sorted(tri_probs.items(), key=lambda x: x[1])
    print(tri_probs)

def generate(lm, limit=1000):
    output = "##"
    while len(output) < limit:
        hist = output[-2:]    # identify bigram history
        candidates = []       # create a list of candidate characters
        weights = []          # create a list of weights according to prob from LM
        for trigram in lm:
            # generate relevant bigram histories and store probabilities
            if trigram[0:2] == hist:
                candidates.append(trigram[-1])
                weights.append(float(lm[trigram]))

        # normalise weights to add up to 1
        weights = [x / math.fsum(weights) for x in weights]

        if len(candidates) == 0:    # if the bigram history has zero probability
            output += "##"           # start a new line
        else:
            # generate random character according to weights
            output += np.random.choice(candidates, size=1, p=weights)[0]
            if output[-1] == "#":  # add another hash symbol for the end of the line
                output += "#"

    return output

def read_lm(f):
    lm = defaultdict(int)
    for line in f:
        lm[line[0:3]] = float(line[4:])
    return lm

def export(lm_file):
    with open(lm_file) as f:
        raw = generate(read_lm(f), 5000).split("##")
        # write the output to a file
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")
        with open((f"{lm_file}_output_{date_time}.txt"), "w") as f:
            for line in raw:
                if line != "":
                    f.write(line+"\n")



if len(sys.argv) < 2 or not (sys.argv[1] != "train" or sys.argv[1] != "generate"):
    print("Usage: ", sys.argv[0], "[train|generate] [source file] ([target file])")
    sys.exit(1)

if sys.argv[1] == "train" and len(sys.argv) != 4:
    print("Usage: ", sys.argv[0], "train [source file] [target file]")
    sys.exit(1)

if sys.argv[1] == "generate" and len(sys.argv) != 3:
    print("Usage: ", sys.argv[0], "train [source file]")
    sys.exit(1)

procedure = sys.argv[1]
source = sys.argv[2]
if len(sys.argv) == 4:
    target = sys.argv[3]

#source = "script.txt"
#target = "rhapsody-lm"

if procedure == "train":
    train(source, target)
elif procedure == "generate":
    export(source)
