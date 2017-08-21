import random
import argparse
from mapping_periods import CLI_MOVES

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", type=int, default=30, help="number of moves to generate")
    return parser.parse_args()

keys = [i for i in CLI_MOVES.keys() if not i.startswith("TURN")]
moves = [b for a, b in CLI_MOVES.items() if not a.startswith("TURN")]

def get_seq(l, choices):
    return (random.choice(choices) for _ in range(l))

def main():
    args = get_args()
    print(" ".join(get_seq(args.l, keys)))

if __name__ == "__main__":
    main()
