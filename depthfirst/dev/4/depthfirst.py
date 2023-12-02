#!/usr/bin/env python3
# coding: UTF-8

"""Implements a simple, naïve depth-first search algorithm which
can be used to find one or all routes through a graph."""

from typing import List, Generator, Tuple


def depthfirst(start: int, finish: int,
               graph: List[List[int]]) -> Generator[List[int], None, None]:
    """Uses slightly less naïve depth-first search to find a
    route out of the Minotaur's maze."""

    stack: List[Tuple[int, List[int]]] = [(start, graph[start])]
    current_room: int = 0
    first_portal: int = 0
    portals: List[int] = []
    visited: List[int] = []

    while stack:
        current_room, portals = stack[-1]
        visited = [X[0] for X in stack]
        portals = [X for X in portals if X not in visited]
        stack[-1] = (current_room, portals)

        if current_room == finish:
            yield visited
        if not portals:
            stack = stack[:-1]
            continue
        first_portal = portals[0]
        stack[-1] = (current_room, portals[1:])
        stack.append((first_portal, graph[first_portal]))


if __name__ == '__main__':
    # +--+--+--+--+
    # |00 01|02 03|
    # +  +--+  +  +
    # |04|05 06|07|
    # +  +  +--+  +
    # |08 09|10 11|
    # +  +  +  +  +
    # |12|13 14|15|
    # +  +  +  +--+
    # |16 17 18 19|
    # +--+--+--+--+

    _MAZE: List[List[int]] = [
        [1, 4],        #  0
        [0],           #  1
        [3, 6],        #  2
        [2, 7],        #  3
        [0, 8],        #  4
        [6, 9],        #  5
        [2, 5],        #  6
        [3, 11],       #  7
        [4, 9, 12],    #  8
        [5, 8, 13],    #  9
        [11, 14],      # 10
        [7, 10, 15],   # 11
        [8, 16],       # 12
        [9, 14, 17],   # 13
        [13, 10, 18],  # 14
        [11],          # 15
        [12, 17],      # 16
        [13, 16, 18],  # 17
        [14, 17, 19],  # 18
        [18]           # 19
    ]
    for route in depthfirst(0, 19, _MAZE):
        print(route)
