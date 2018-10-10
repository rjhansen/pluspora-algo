#!/usr/bin/python3
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
+ + +_+-+
|Q R S T|
+-+-+-+-+

An example of a valid path from A to T would be AEIJFGCDHLONRST.
Another valid path is AEIMQRST.  A depth-finding algorithm needs
to only find _a_ valid path; exhaustive depth-finding will find
the _optimal_ valid path.

For right now let's focus on the simple case."""


from typing import Dict, List

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

def depthfirst(start: str, finish: str) -> str:
    """Uses slightly less naïve depth-first search to find a
    route out of the Minotaur's maze."""

    stack: List[List[str, List[str]]] = [[start, list(_MAZE[start])]]
    current_room: str = ""
    first_portal: str = ""
    portals: List[str] = []
    visited: List[str] = []

    while stack:
        current_room, portals = stack[-1]
        visited = [X[0] for X in stack]
        portals = [X for X in portals if X not in visited]
        stack[-1] = [current_room, portals]

        if current_room == finish:
            break
        if not portals:
            stack = stack[:-1]
            continue
        first_portal = portals[0]
        stack[-1] = [current_room, portals[1:]]
        stack.append([first_portal, list(_MAZE[first_portal])])

    return ''.join([X[0] for X in stack])

if __name__ == '__main__':
    print(depthfirst("A", "T"))
