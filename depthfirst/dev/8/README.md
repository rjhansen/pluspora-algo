# Pruning

## History

* [Installment 1](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/1)
* [Installment 2](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/2)
* [Installment 3](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/3)
* [Installment 4](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/4)
* [Installment 5](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/5)
* [Installment 6](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/6)
* [Installment 7](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/7)

## Overview

There are two reasons why our 5x5 board gets searched so slowly:

* The number of routes between `(start, end)` grows _exponentially_
* Most of these routes are lousy

We tackle this by _pruning the tree_.  Tree pruning is what escalates depth-first search from brute force and ignorance into AI.  Tree pruning techniques can get really complicated, but we'll step into them one bit at a time.

The simplest technique is called _partial path validation_.  For many problems, we can tell whether a snippet of a proposed solution makes sense.  For instance, if I were to propose `qrfxv` as part of an English word you could quickly reject it, as English has no words where `q` is followed by `r`.

Consider the following board:

```
Q U T
D E U
X T E
```

Starting from `Q` and moving down to `D`, we realize this matches no English word — so we abort further searching, thus saving us many paths we know to be dead ends.

## What needs to be done

Implementing partial path validation requires us to tweak our depth-first engine very slightly:

### depthfirst.py

```python
def depthfirst(start: int, finish: int,
               graph: List[List[int]],
               accept_func=lambda x: True,
               pv_func=lambda x: True) -> List[int]:
    """Uses slightly less naïve depth-first search to find a
    route out of the Minotaur's maze."""

    # snip snip snip

    while stack:
        # snip snip snip
        if not pv_func(visited):
            stack = stack[:-1]
            continue
        if current_room == finish:
            if accept_func(visited):
                yield visited
            stack = stack[:-1]
            continue
```

`pv_func` is shorthand for 'partial validation function', and it works quite simply.  If our current route cannot yield a result, then we back out one step and resume searching.

Actually implementing a partial validator for Boggle is likewise not much trouble:

### Tweaking our Boggle solver

With the tweaked API, our Boggle solver requires only a trivial change … and a few new functions to support our trivial change.

```python
(graph, table) = _make_board(board)
node_count: int = len(graph)
for start in range(0, node_count):
    for end in range(0, node_count):
        for path in depthfirst(start, end, graph,
                               accept_func, pv_func):
            yield ''.join([table[X] for X in path])
```

#### Finding an insertion point

To test a partial word to see if it could be real, we just find where in the dictionary the current fragment would go.  If our partial path matches whatever word we find at the insertion point, then we're good.

```python
def find_insertion_point(word: str) -> int:
    left: int = 0
    right: int = len(_WORDS)
    while left < right:
        midpoint: int = int((left + right) / 2)
        if word <= _WORDS[midpoint]:
            right = midpoint
        else:
            left = midpoint + 1
    return int((left + right) / 2)
```

#### The partial validator

```python
def pv_func(sofar: List[int]) -> bool:
    word: str = ''.join([table[X] for X in sofar])
    insert_at: int = find_insertion_point(word)

    return (insert_at < len(_WORDS) and
            word == _WORDS[insert_at][:len(word)])
```

We check whether the insertion point occurs after the end of our word list because it's possible for the insert-before point to occur after the last word in our dictionary.

#### The full validator

We can now rewrite the acceptance function in terms of the partial validator:

```python
def accept_func(answer: List[int]) -> bool:
    word: str = ''.join([table[X] for X in answer])
    insert_at: int = find_insertion_point(word)

    return (insert_at < len(_WORDS) and
            _WORDS[insert_at] == word)
```

## Performance

Our `pytest` script now runs in 0.15 seconds, for a speedup of 37,300%!

## Conformance

### pylint

No errors and full marks.

### pep8

No errors and full marks.

### pytest

No errors.
