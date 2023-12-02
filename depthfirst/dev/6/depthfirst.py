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
            stack = stack[:-1]
            continue
        if not portals:
            stack = stack[:-1]
            continue
        first_portal = portals[0]
        stack[-1] = (current_room, portals[1:])
        stack.append((first_portal, graph[first_portal]))
