# The Minotaur's Revenge

## History

* [Installment 1](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/1)
* [Installment 2](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/2)
* [Installment 3](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/3)

## PEP8

Python Enhancement Proposal #8 specifies how Python code should be laid out, and the `pycodestyle` tool helps automate testing code for conformance to PEP8.  Since we have this tool it would be a crying shame to not use it.  All examples from here on out will have a `Conformance` section, where any deviations from PEP8 will be noted.

## The Minotaur

The Minotaur's current dastardly way of keeping us from leaving the maze: giving us a maze with more than 26 rooms.  Our current system can't handle mazes that large.  We need to be able to reach _at least_ mazes ten on a side.

## What's next?

Our maze traverser is a neat proof of concept, but there are at least three major problems we need to solve before this could be useful to anyone but us.  We need to:

* remove the hardcoded maze and let users provide their own, and
* make it possble for users to provide mazes with more than 26 rooms, and
* return as few or as many different routes as the user wishes

### Removing the hardcoded maze

Solving the first is easy: add another parameter to `depthfirst` called `graph`, which will contain the graph to search.


### Supporting large mazes
Instead of having a `Dict[str, str]` mapping single-letter room names to a string of single-letter adjacent rooms we can switch to a `List[List[int]]`.  The zeroth element of this list will be a list of what other rooms are adjacent to room zero; the first element of this list will be a list of what other rooms are adjacent to room one; and so on.  This is easier to show than to explain, so take a look at the code around line 37:

```python
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
```

We now support arbitrarily-sized mazes, limited only by your system's RAM.

### Returning more than one path
As it currently stands we bomb out as soon as we find one path.  We could pretty easily adjust our code to return _all_ paths, but that could become unpleasant quickly: how many paths could there be through a maze a thousand squares on a side?  We might wind up creating an unpleasantly large data object.

In most programming languages we'd add another parameter to `depthfirst` giving a maximum number of paths to return.  This is sort of a solution, but not really: what if, after calling `depthfirst`, we wanted to "go back where we left off" and get another block of paths?

It turns out Python allows us to do this through what are, in effect, resumable functions.  They look and act much like normal functions except they use the `yield` statement to return a value, rather than `return`.  When using `return`, that tells the Python environment "we're done here, clean up everything".  When using `yield`, that tells the Python environment "we might be using this later, so save our current state."

(Behind-the-scenes, this is called a _generator_ that uses _lazy evaluation._  But let's avoid the complicated terms for now, and just work on using it like a resumable function.)

Our resumable function looks almost exactly the same as our original.  The major change comes from how (a) we no longer have a `return` statement at the end, and (b) each time we discover a path we `yield` it back to the caller.

```python
if current_room == finish:
    yield visited
```

Then, in the main core of our program, it looks like:

```python
if __name__ == '__main__':

    # some intervening stuff is elided here

    for route in depthfirst(0, 19, _MAZE):
        print(route)
```

You might be tempted to think, "But it looks there like `depthfirst` is returning a list!  We're iterating over it as if it were one.  Weren't we trying to avoid returning an arbitrarily huge list of paths?"

And you're almost right… almost!  It's not that we iterate over this as if it were a list: it's that we iterate over lists as if it were this.

When you iterate over a list, behind-the-scenes Python says "all right, I'll grab the first element from the list and pass it on to this loop… I'll grab the next element and pass it…", one at a time.  Python iterates over _sequences,_ not lists.  Anything that presents a sequence of values can be used in a `for` loop.

And since a generator is a resumable function, and can create one value after another as we wish, that means generators can be used in `for` loops.  And in this way we can write millions or billions of routes to standard output without having to create a data structure to contain them all.  We return (actually, `yield`) one path at a time until all the paths are exhausted and our generator finishes.

## What we accomplished

* We **made it more general** by removing our hardcoded maze and switching from a `Dict[str, str]` to a `List[List[int]]`.
* We **support larger mazes** by switching to a generator, which lets us get one path or a million paths without requiring an extremely large data structure

## Unit testing

We're reaching a point where we've got something worth writing unit tests for.  Those will be introduced in the next installment.  Stay tuned!

## Conformance

### pylint

No errors and full marks.  (Note that this doesn't mean we're bug-free.  It just means we're free of the easy bugs `pylint` was designed to find.)

### pycodestyle

`pycodestyle` tells us we're violating PEP8 guideline E262, which says that comments should begin with a hashmark and a single space.  In some of our comments we violate this rule in order to make numbers line up nicely, so we've got a good reason for this violation.  Re-running it with `pycodestyle --ignore=E262 depthfirst.py` yields no other problems.

## Next steps

In the next installment, we'll cover unit testing with `pytest` and another way the Minotaur is tricking us into staying in the maze.