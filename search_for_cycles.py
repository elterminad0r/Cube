import argparse
import sys
import random
from collections import deque
from functools import reduce
from mapping_periods import test_loops_nonr
from cube import FINALMAPPINGS

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", type=int, default=100, help="sequence length")
    parser.add_argument("-r", "--repetitions", type=int, default=100, help="sequence length")
    parser.add_argument("-s", "--start", type=int, default=0, help="starting threshold")
    parser.add_argument("-p", "--progress", action="store_true", help="show progress")
    parser.add_argument("-v", "--verbose", action="store_true", help="show sequence with progress")
    parser.add_argument("-o", "--old-school", action="store_true", help="use old school full enumeration")
    parser.add_argument("-u", "--update", action="store_true", help="alert when new highest is found")
    parser.add_argument("-m", "--methodical", action="store_true", help="methodically generate move sets - ignores repeats")
    return parser.parse_args()

moves = [(a, b) for a, b in FINALMAPPINGS.items() if not a.startswith("TURN")]

#transform tuples into mapping list and string
def translate_seq(seq):
    return reduce((lambda a, b: a | b), (i[1] for i in seq)), " ".join(i[0] for i in seq)

#generate random sequences
def random_seqs(repeats, l):
    for _ in range(repeats):
        seq = [random.choice(moves) for _ in range(l)]
        yield translate_seq(seq)

#full alphabetical generator
def full_methodical_seqs(l, stack=deque()):
    if l:
        for i in moves:
            stack.append(i)
            yield from full_methodical_seqs(l-1, stack)
            stack.pop()
    else:
        yield translate_seq(stack)

rot_moves = [(a, b) for a, b in moves if a[0] in "UD"]
desc_moves = [(a, b) for a, b in moves if a[0] == "F"]

#sets first non U or D move to F
def rotational_methodical_seqs(l, stack):
    if l:
        for i in rot_moves:
            stack.append(i)
            yield from rotational_methodical_seqs(l-1, stack)
            stack.pop()
        for i in desc_moves:
            stack.append(i)
            yield from full_methodical_seqs(l-1, stack)
            stack.pop()
    else:
        yield translate_seq(stack)

#sets first move to U
def limited_methodical_seqs(l):
    move, = [(a, b) for a, b in moves if a == "U"]
    yield from rotational_methodical_seqs(l-1, deque([move]))

def search(repeats, thresh, p, space, v, u):
    longest_seq = None
    longest = thresh
    try:
        for i, (seq, exp) in enumerate(space):
            try:
                if p:
                    sys.stdout.write(" " * 20 + "\r{:>5.2f}% ({})".format(i / repeats * 100, i))
                    if v:
                        sys.stdout.write(" current seq {}".format(exp))
                n = test_loops_nonr(seq)
                if n > longest:
                    longest = n
                    longest_seq = exp
                    if u:
                        sys.stdout.write(" " * 20 + "\rnew longest sequence is {},\nlength {}\n".format(longest_seq, longest))
            except KeyboardInterrupt:
                sys.stdout.write(" " * 20 + "\r{:>5.2f}% ({})".format(i / repeats * 100, i, exp))
                if v:
                    sys.stdout.write(" current seq {}".format(exp))
                sys.stdout.write(" NOW PAUSED")
                input()
    except KeyboardInterrupt:
        pass
    print("\rfinal result: sequence {}\nhas length {}".format(longest_seq, longest))

def main():
    args = get_args()
    if args.methodical and args.old_school:
        raise ValueError("only one of -m and -o should be switched on")
    if args.methodical:
        space = limited_methodical_seqs(args.length)
        reps = len(moves) ** (args.length - 1) // 3
    elif args.old_school:
        space = full_methodical_seqs(args.length)
        reps = len(moves) ** args.length
    else:
        space = random_seqs(args.repetitions, args.length)
        reps = args.repetitions
    print("length {}, reps {}".format(args.length, args.repetitions))
    print("start is {}".format(args.start))
    search(reps, args.start, args.progress, space, args.verbose, args.update)

if __name__ == "__main__":
    main()
