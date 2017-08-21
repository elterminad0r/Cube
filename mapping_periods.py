import argparse
import timeit
import re
import time
from fractions import gcd
from functools import reduce
from cube import *

def lcm(a, b):
    return a * b // gcd(a, b)

def cli_friendly(move):
    return move.replace("'", '-').replace(' ', '_')

CLI_MOVES = {cli_friendly(a): b for a, b in FINALMAPPINGS.items()}

def get_args(tests):
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sequence", nargs="+", type=str, choices=CLI_MOVES, help="series of moves on cube")
    parser.add_argument("-i", "--input", type=argparse.FileType("r"), default="-", help="file to read input sequence from if -s is omitted")
    parser.add_argument("-f", "--functions", nargs="+", type=str, default=["nonrec"], choices=tests, help="functions to run")
    parser.add_argument("-c", "--compare", action="store_true", help="run comparisons between functions")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose - display sequence")
    parser.add_argument("-p", "--print-cube", action="store_true", help="print move as cube")
    parser.add_argument("-d", "--display", action="store_true", help="display input sequence")
    parser.add_argument("-t", "--time", action="store_true", help="show time taken to simplify moves")
    parser.add_argument("-n", "--no_evaluate", action="store_true", help="do not show loop values")
    parser.add_argument("-r", "--repeats", action="store", type=int, default=1000, help="repeats with -c")
    return parser.parse_args()

def test_cube(simple, v=False):
    cube = Cube()
    start = cube.squares
    i = 1
    cube.transform(simple)
    while start != cube.squares:
        i += 1
        cube.transform(simple)
    return i

def test_cubeless(simple, v=False):
    start = simple
    tgt = list(range(54))
    i = 1
    while start.map != tgt:
        i += 1
        start |= simple
    return i

def investigate_loop(seq, ind, start_ind, indices, d=1):
    if ind == start_ind:
        return d
    else:
        indices.add(seq[ind])
        return investigate_loop(seq, seq[ind], start_ind, indices, d + 1)

def find_loops(seq):
    lens = []
    used = set()
    for ind, i in enumerate(seq):
        if ind not in used:
            used.add(ind)
            lens.append(investigate_loop(seq, seq[ind], ind, used))
    return lens

def test_loops(simple, v=False):
    return reduce(lcm, find_loops(simple.map))

def test_loops_nonr(seq, v=False):
    simple = seq.map
    lens = []
    used = set()
    for ind, i in enumerate(simple):
        if ind not in used:
            used.add(ind)
            d = 0
            x = ind
            while x != ind or d == 0:
                x = simple[x]
                used.add(x)
                d += 1
            lens.append(d)
    if v:
        print("loops are {}".format(lens))
    return reduce(lcm, lens)

tests = {"cube": test_cube,
         "chain": test_cubeless,
         "loops": test_loops,
         "nonrec": test_loops_nonr}

def test_times(seq, to_test, rep):
    for a, b in tests.items():
        if a in to_test:
            test = b
            print("time with {}: ".format(a), end="")
            print(timeit.timeit(stmt="test(seq)", globals=locals(), number=rep))

def main():
    args = get_args(tests)
    if args.sequence:
        moves = args.sequence
    else:
        with args.input as inputfile:
            moves = inputfile.read().strip().split()
    seq = [CLI_MOVES[i] for i in moves]
    start = time.time()
    simple = reduce(Mapping.__or__, seq)
    if args.time:
        print("chaining sequence took {}s".format(time.time() - start))
    if args.display:
        print("input sequence was {}".format(moves))
        print("reduces to {}".format(simple))
    if args.print_cube:
        cu = Cube()
        cu.transform(simple)
        print("result of sequence on a cube:")
        print(cu)

    functions = args.functions
    if args.compare:
        test_times(simple, functions, args.repeats)
    if not args.no_evaluate:
        for a, b in tests.items():
            if a in functions:
                print("value with {} is {}".format(a, b(simple, args.verbose)))

if __name__ == "__main__":
    main()
