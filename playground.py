from functools import reduce
from cube import *

EXIT_WORDS = set("EXIT STOP CANCEL SURRENDER".split())
HELP_WORDS = set("HELP MOVES MENU INVENTORY".split())
RESET_WORDS = set("RESET RESTART RETRY FRESH NEW".split())
HELP_TEXT = """\
Hello! Welcome to the cube simulator. This is a simple sandbox allowing you to manipulate the cube.
You can enter any of the following single letters to perform as a move:
F ront
B ack
U p
D own
L eft
R ight
These will rotate this face clockwise. The upper right tells you which face is which, if you need.
You can invert a move by adding a ' to the end - for example F' rotates the front face anticlockwise.
You can also manipulate the cube. You can write "turn left" to turn the cube left, so the the R face becomes F.
Other available directions: right, up, down, CW and ACW. (clockwise and anticlockwise, where face F stays in place)
You can summon this menu with "help". Lastly, you can exit with "exit". Have fun!\
"""

class CubeReset(Exception):
    pass

class InputError(Exception):
    pass

#read a move
def readmove(inp):
    if inp in FINALMAPPINGS:
        return FINALMAPPINGS[inp]
    elif inp in EXIT_WORDS:
        raise KeyboardInterrupt
    elif inp in HELP_WORDS:
        print(HELP_TEXT)
        return readmove()
    elif inp in RESET_WORDS:
        raise CubeReset
    else:
        print("the input {!r} should be one of {}".format(inp, FINALMAPPINGS.keys()))
        raise InputError

def readmoves():
    inp = input("enter move ([UDFBLR]'?|turn (left|right|up|down)) > ").upper().split()
    try:
        return reduce(Mapping.__or__, (readmove(i) for i in inp))
    except InputError:
        return readmoves()

def main():
    cube = Cube()
    try:
        while True:
            print(cube)
            try:
                inp = readmoves()
                cube.transform(inp)
            except CubeReset:
                cube = Cube()
    except (KeyboardInterrupt, EOFError):
        print("bye")

if __name__ == "__main__":
    main()
