#!/usr/bin/env python3
# coding: UTF-8

"""Implements a simple, naïve depth-first search algorithm which
will be used to solve the following simple maze.

+-+-+-+-+
|A B|C D|
+ +-+ + +
|E|F G|H|
+ + +-+ +
|I J|K L|
+ + + + +
|M|N O|P|
+ + + +-+
|Q R S T|
+-+-+-+-+

An example of a valid path from A to T would be AEIJFGCDHLONRST.
Another valid path is AEIMQRST.  A depth-finding algorithm needs
to only find _a_ valid path; exhaustive depth-finding will find
the _optimal_ valid path.

For right now let's focus on the simple case."""


from typing import Dict

_MAZE: Dict[str, str] = {
    "A": "BE",
    "B": "A",
    "C": "GD",
    "D": "CH",
    "E": "AI",
    "F": "GJ",
    "G": "FC",
    "H": "DL",
    "I": "EMJ",
    "J": "FIN",
    "K": "LO",
    "L": "KHP",
    "M": "IQ",
    "N": "JOR",
    "O": "NKS",
    "P": "L",
    "Q": "MR",
    "R": "QNS",
    "S": "ROT",
    "T": "S"
}

def depthfirst(current: str, finish: str, rope:str=""):
    """Uses naïve depth-first search to find an optimal route
    out of the Minotaur's maze."""

    rope += current

    if current == finish:
        return rope

    portals = [X for X in _MAZE[current] if X not in rope]

    for portal in portals:
        route = depthfirst(portal, finish, rope)
        if route:
            return route

    return None

if __name__ == '__main__':
    print(depthfirst("A", "T"))
