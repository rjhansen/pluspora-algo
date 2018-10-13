#!/usr/bin/env python3
# coding: UTF-8

"""Solves a given Boggle board... quickly."""


from io import TextIOWrapper
from re import compile as re_c
from typing import List
from zipfile import ZipFile
from depthfirst import depthfirst


def _populate_words() -> List[str]:
    ret_val: List[str] = []
    regex = re_c("^[a-z]{3,}$")
    with ZipFile("words.zip") as zipf:
        with zipf.open("words") as handle:
            for line in TextIOWrapper(handle, encoding="UTF-8"):
                line = line.strip()
                if regex.match(line):
                    ret_val.append(line)
    return sorted(ret_val)


_WORDS = _populate_words()


def solve(board: str) -> str:
    """Given a rectangular grid of letters represented
    as a single string with embedded \ns, iterate over
    the board yielding valid Boggle words."""

    def accept_func(result: List[int]):
        as_letters = [table[X] for X in result]
        word = ''.join(as_letters)
        return word in _WORDS

    def pv_func(sofar: List[int]):
        as_letters = [table[X] for X in sofar]
        word = ''.join(as_letters)

        left = 0
        right = len(_WORDS)
        while left < right:
            midpoint = int((left + right) / 2)
            if word <= _WORDS[midpoint]:
                right = midpoint
            else:
                left = midpoint + 1
        insertion_point = int((left + right) / 2)

        if insertion_point >= len(_WORDS):
            return False
        insert_before = _WORDS[insertion_point]
        if len(word) <= len(insert_before):
            if word == insert_before[:len(word)]:
                return True
        return False

    (graph, table) = _make_board(board)
    node_count: int = len(graph)
    for start in range(0, node_count):
        for end in range(0, node_count):
            for path in depthfirst(start, end, graph,
                                   accept_func, pv_func):
                yield ''.join([table[X] for X in path])


def _make_board(input_str: str) -> (List[List[int]], List[str]):
    def make_grid(row_c: int, col_c: int) -> List[List[int]]:
        maze: List[List[int]] = []
        for row in range(0, row_c):
            thisrow = []
            for col in range(0, col_c):
                adjacent = []
                if row != 0:
                    adjacent.append((col_c * (row-1)) + col)
                if row != rows - 1:
                    adjacent.append((col_c * (row+1)) + col)
                if col != 0:
                    adjacent.append((row * col_c) + col - 1)
                if col != cols - 1:
                    adjacent.append((row * col_c) + col + 1)
                thisrow.append(adjacent)
            maze += thisrow
        return maze

    def sanity_check() -> (int, int):
        rows = input_str.split("\n")
        rows = [X.strip() for X in rows]
        for row in rows[1:]:
            if len(row) != len(rows[0]):
                raise Exception("jagged board")
        return (len(rows), len(rows[0]))

    rows: int = 0
    cols: int = 0
    (rows, cols) = sanity_check()
    graph: List[List[int]] = make_grid(rows, cols)
    lookup_table = list(input_str.lower().replace("\n", ""))
    lookup_table = ["qu" if X == "q" else X for X in lookup_table]
    return (graph, lookup_table)
