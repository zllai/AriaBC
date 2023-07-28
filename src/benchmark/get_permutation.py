import argparse
import random
import sys
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=str)
    opt = parser.parse_args()

    f = open(opt.spec)
    steps = []
    for line in f:
        tokens = re.split(" |\t", line)
        if tokens[0] == "step":
            steps.append(tokens[1])
    print("permutation " + " ".join(steps))


