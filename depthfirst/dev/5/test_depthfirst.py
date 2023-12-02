#!/usr/bin/env python3
# coding: UTF-8

"""Implements a variety of unit tests for our depth-first
path finding algorithm."""


from typing import List, Set
from depthfirst import depthfirst


def _make_maze(size: int) -> List[List[int]]:
    """Creates a square maze of a given size where each
    room is connected to the four adjacent ones."""

    maze: List[List[int]] = []
    for row in range(0, size):
        thisrow = []
        for col in range(0, size):
            adjacent = []
            if row != 0:
                adjacent.append((size * (row-1)) + col)
            if row != (size - 1):
                adjacent.append((size * (row+1)) + col)
            if col != 0:
                adjacent.append((row * size) + col - 1)
            if col != size - 1:
                adjacent.append((row * size) + col + 1)
            thisrow.append(adjacent)
        maze += thisrow
    return maze


def test_depthfirst_no_repeats() -> None:
    """Creates mazes and tests them to ensure that for each
    generated path, each step in the path is valid, no rooms
    are repeated within a given path, and each path generated
    is unique."""

    for size in range(2, 6):
        foundset: Set[str] = set()
        maze: List[List[int]] = _make_maze(size)
        for route in depthfirst(0, (size**2) - 1, maze):
            # Ensure each room is accessible via the one
            # preceding it.
            for index in range(1, len(route)):
                assert route[index] in maze[route[index-1]]

            # Converting a list to a set, and comparing
            # the two sizes, is a good way to quickly test
            # whether there are repeated elements.
            assert len(set(route)) == len(route)

            # A list can be converted into a set, but a list
            # cannot be put *into* a set.  So we convert our
            # route into a string, see whether that's in our
            # set of found paths, and so on.
            as_string: str = '-'.join([str(X) for X in route])
            assert as_string not in foundset
            foundset.add(as_string)
