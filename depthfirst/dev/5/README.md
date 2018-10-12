# Unit Tests

## History

* [Installment 1](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/1)
* [Installment 2](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/2)
* [Installment 3](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/3)
* [Installment 4](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/4)

## Why unit test?

Unit testing is one of the fundamental tools of software engineering.  A good rule of thumb is that until your unit tests are written, documented, and successfully run, you have no business sharing your code with anyone — not even your in-house QA testers.  Unit testing is what turns things from "I have a hunch it works" to "I have some evidence it works".

## Unit testing our maze traverser

Several things go into success.  Our traverser must:

* Find all valid paths
* Find no invalid paths
* Find only non-repeating paths
* Find unique paths

To be 100% sure of any of these would require formal software verification.  That's obnoxious, difficult, and expensive.  Unit testing can't prove universal statements like "will find all" or "will never find" or "will only ever".  Unit testing is, by nature, more limited.  Let's try it again: for purposes of unit testing, our traverser must:

* Generate at least one valid path if any paths exist
* 'Valid' is defined as:
  * No repeated rooms
  * Each room (save the first) is accessible from the one before it
* If more than one valid path is generated, it must not repeat a prior path

Now that we have a solid idea of what we're testing, let's introduce unit testing with `pytest`!

## Pytest

`pytest` is a set of Python programs that may be packaged for your distro, or else can be installed through `pip`.

* Ubuntu: `sudo apt install python3-pytest`
* Others: check your distro, or, `sudo -H python3 -m pip install pytest`

With that out of the way, let's learn by doing and dive into our unit tester.

## test_depthfirst.py

By convention, unit tests are dropped into their own files.  So open up an editor and create `test_depthfirst.py`.

```python
#!/usr/bin/env python3
# coding: UTF-8

"""Implements a variety of unit tests for our depth-first
path finding algorithm."""


from typing import List, Set
from depthfirst import depthfirst
```

The only thing here that might be worth noting is our `from depthfirst import depthfirst`.  Essentially it's saying, "look inside `depthfirst.py`, which is located in this same directory, and make its `depthfirst` function available to us."

```python
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
```

For testing purposes we'll need a variety of mazes of different sizes, so we've written a function that will make empty mazes — no interior walls, etcetera — of a given size.  Following our convention, we prefix the function name with an underscore to mark it as being for our use only.

```python
def test_depthfirst_no_repeats():
    """Creates mazes and tests them to ensure that for each
    generated path, each step in the path is valid, no rooms
    are repeated within a given path, and each path generated
    is unique."""

    for size in range(2, 6):
        foundset: Set[str] = set()
        maze: List[List[int]] = _make_maze(size)
        for route in depthfirst(0, (size**2) - 1, maze):
```

Finally, our unit test.  Each test function name must begin with `test_`.  Within it, for each maze of size 2, 3, 4, and 5, we find paths from the top left to the bottom right.  For each path we discover we perform the following tests:

```python
            for index in range(1, len(route)):
                assert route[index] in maze[route[index-1]]
```

Is the path properly connected?  We `assert` that room N is connected to room N-1.  If it's not then the path is wrong.

```python
            assert len(set(route)) == len(route)

```

Are there any repetitions in this path?  A `list` can be converted into a `set`, which is sort of like a list that's been stripped of duplicate entries.  (It has other features, too, but they're not relevant here.)  So if the size of a set version of our path is the same as the size of our path, our path has no duplicates.

```python
            as_string: str = '-'.join([str(X) for X in route])
            assert as_string not in foundset
            foundset.add(as_string)
```

Python sets are neat, but they require the object placed into them support hashing.  Python lists are not hashable.  Strings, on the other hand, are.  So we convert a list of `[1, 2, 3]` into the string `"1-2-3"` and check to see if we've already seen it.  If we have, then we're not generating unique paths.  If we haven't, add it to the set of found paths and continue.

## Results

We run our unit tests by simply typing `pytest-3` in the same directory as our code.  (If you installed it through `pip` it might be called just `pytest`.)  Running it shows us:

```
__________________________ test_depthfirst_no_repeats __________________________

    def test_depthfirst_no_repeats():
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
>               assert as_string not in foundset
E               AssertionError: assert '0-2-3' not in {'0-2-3'}

test_depthfirst.py:59: AssertionError
=========================== 1 failed in 0.02 seconds ===========================
```

Well, _crap._  We're generating redundant paths.  Time for us to go back to the drawing board…

## Conformance

### pylint

No errors and full marks.  Our unit testing revealed a bug, but `pylint` didn't.  Take this as a lesson: `pylint` is a useful tool but it cannot save you from yourself.

### pep8

No errors and full marks.

## Next steps

Clearly, finding the %$!@ bug.