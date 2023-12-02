# It Boggles The Mind

**STOP.** Make sure you understand how depth-first search works, both [generally speaking](https://en.wikipedia.org/wiki/Depth-first_search) and our particular implementation of it.

**WARNING.** Although this installment works, it has serious performance issues.  Expect them and don't beat yourself up over them.  We'll fix them soon.

## History

* [Installment 1](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/1)
* [Installment 2](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/2)
* [Installment 3](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/3)
* [Installment 4](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/4)
* [Installment 5](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/5)
* [Installment 6](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/6)

## Overview

As it happens, virtually every game can be represented as a graph where a node represents the state of play and an edge represents a choice in how one plays.  Some games have graphs so large it's absurd to approach them graph-theoretically (go).  Some have graphs so small it requires nothing in the way of AI techniques to play them perfectly (tic-tac-toe).

In between those two extremes lies a continuum of games from Boggle (requires simple tree pruning) to Scrabble (genetic algorithms) and chess (the whole shebang).

We're going to start simply, with Boggle.

## What needs to be done

Given a Boggle board represented as a string, we need to:

* figure out the dimensions of the board
* create a graph of that size
* create a lookup table that converts node numbers into letters
* for each pair of squares in the board, compute all paths between them
* for each path, if it corresponds to a word yield the word back to the caller

You'll need `words.zip` from the GitHub repo.

Let's sling some code.  Open up `boggle.py` in the same directory as `depthfirst.py`:

## Loading our dictionary
```python
from io import TextIOWrapper
from re import compile as re_c
from typing import List, Set, Tuple, Generator
from zipfile import ZipFile
from depthfirst import depthfirst


def _populate_words() -> Set[str]:
    ret_val: Set[str] = set()
    regex = re_c("^[a-z]{3,}$")
    with ZipFile("words.zip") as zipf:
        with zipf.open("words") as handle:
            for line in TextIOWrapper(handle, encoding="UTF-8"):
                line = line.strip()
                if regex.match(line):
                    ret_val.add(line)
    return ret_val


_WORDS = _populate_words()
```

Since our dictionary-loading function is private to us, we prefix it with an underscore.  (This is the last time the significance of the initial underscore will be mentioned; you're responsible for knowing it from here on out.)

`regex` is a variable holding a compiled regular expression corresponding to a valid Boggle word (no proper nouns, no apostrophes, minimum length of three letters, etc.).  If you don't understand regular expressions, stop reading this and go learn them.  They are fundamental programming tools.

The `with` syntax is Python's way of grabbing a limited resource in such a way that when we're done with the resource we automatically release it.  First we open the ZIP file, then we open a specific file within that archive.  Using the handle to our desired file, we use TextIOWrapper to read in lines of UTF-8 text.

## Sanity checking our input

```python
def sanity_check() -> Tuple[int, int]:
    rows = input_str.split("\n")
    rows = [X.strip() for X in rows]
    for row in rows[1:]:
        if len(row) != len(rows[0]):
            raise Exception("jagged board")
    return (len(rows), len(rows[0]))
```

"Wait," you might say: "it has no docstring, and are you sure you want to export it?"  Good catch, grasshopper.  Remember those two questions: they willl be answered later.

## Making a rectangular graph

```python
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
```

"Wait," you might say, "I have those same questions — and didn't you just steal this from the unit test you wrote a bit ago?"

Hold onto your questions.  But yes, yes I did.

## Making the board and lookup table

```python
def _make_board(input_str: str) -> (List[List[int]], List[str]):
    def make_grid(row_c: int, col_c: int) -> List[List[int]]:
        # snipped: see above

    def sanity_check() -> (int, int):
        # snipped: see above

    rows: int = 0
    cols: int = 0
    (rows, cols) = sanity_check()
    graph: List[List[int]] = make_grid(rows, cols)
    lookup_table = list(input_str.lower().replace("\n", ""))
    lookup_table = ["qu" if X == "q" else X for X in lookup_table]
    return (graph, lookup_table)
```

You see, grasshopper, in Python functions may be defined within functions.  `make_grid` and `sanity_check` are only visible within `_make_board`: for that reason they're inherently private.  And while docstrings are always a good idea, they're less essential for functions that are never exposed to end-users.

The only thing here that might be unexpected is Python's ternary-if expression.  `X if Y else Z` is equivalent to `Y ? X : Z` in most C-derived languages.  That list comprehension in essence says, "for each letter in our table, if it's a 'Q' change it to a 'QU'."  This is per standard Boggle rules, where a 'U' is assumed to be immediately following each 'Q'.

## Playing Boggle

```python
def solve(board: str) -> str:
    """Given a rectangular grid of letters represented
    as a single string with embedded \ns, iterate over
    the board yielding valid Boggle words."""

    (graph, table) = _make_board(board)
    node_count: int = len(graph)
    for start in range(0, node_count):
        for end in range(0, node_count):
            for path in depthfirst(start, end, graph):
                as_letters = [table[X] for X in path]
                word = ''.join(as_letters)
                if word in _WORDS:
                    yield word
```

Now we're getting somewhere!  For each pair of nodes, find all possible paths between them.  Convert each path to a word, and if it's in our word set, `yield` it back to the caller!

Hmmm.

You know, come to think of it, wouldn't it be nice if the engine itself was capable of evaluating acceptance criteria?

Yeah, let's do that.

## Hacking the engine

Change `depthfirst` in `depthfirst.py` to be:

```python
def depthfirst(start: int, finish: int,
               graph: List[List[int]],
               accept_func=lambda x: True) -> Generator[List[int], None, None]:

# much stuff omitted
        if current_room == finish:
            if accept_func(visited):
                yield visited
            stack = stack[:-1]
            continue
# much more stuff omitted
```

Change our `solve` to be:

```python
def solve(board: str) -> Generator[str, None, None]:
    """Given a rectangular grid of letters represented
    as a single string with embedded \ns, iterate over
    the board yielding valid Boggle words."""

    def accept_func(result: List[int]):
        as_letters = [table[X] for X in result]
        word = ''.join(as_letters)
        return word in _WORDS

    (graph, table) = _make_board(board)
    node_count: int = len(graph)
    for start in range(0, node_count):
        for end in range(0, node_count):
            for path in depthfirst(start, end, graph, accept_func):
                yield ''.join([table[X] for X in path])
```

There, much cleaner.  Now all we need is a `test_boggle.py` and…

```python
#!/usr/bin/env python3
# coding=UTF-8

"""Provides unit testing for the Boggle solver."""


from boggle import solve


def test_boggle():
    """Checks for twelve known words in a specific board."""
    board = """CATER
XLUAW
BDFGH
IJKMN
OPQST"""
    known_words = set(["cat", "cater", "caterwaul", "ate", "tea",
                       "eta", "late", "lute", "later", "wag",
                       "jib", "poi"])
    found_words = set()
    for word in solve(board):
        assert word in known_words
        found_words.add(word)
    assert known_words == found_words
```

We're done.  How long will it take our Boggle solver to discover twelve words hidden in a five by five grid?

```
============================= test session starts ==============================
platform linux -- Python 3.6.6, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
rootdir: /home/rjh/Projects/algorithms/depthfirst/dev/7, inifile:
plugins: pylint-0.8.0, pep8-1.0.6
collected 1 item                                                               

test_boggle.py .                                                         [100%]

========================== 1 passed in 56.40 seconds ===========================
```

56 seconds?  That's _horrible!_  We can do better than that.

## Conformance

### pylint

No errors and full marks.

### pycodestyle

No errors and full marks.

### mypy

No errors and full marks.

### pytest

No errors.
