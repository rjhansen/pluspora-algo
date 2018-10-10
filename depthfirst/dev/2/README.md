# Iteration 2

## Recap

* Iteration 1: [code](https://github.com/rjhansen/pluspora-algo/blob/master/depthfirst/dev/1/depthfirst.py), [walkthrough](https://github.com/rjhansen/pluspora-algo/blob/master/depthfirst/dev/1/README.md)


## Where We Are Now…

The Minotaur has a filthy trick up his sleeve: his maze is _huge,_ a thousand grid squares across by a thousand high.  With routes possibly a million letters long requiring a million recursive calls, your poor little Python interpreter has lost its fragile little mind.

Speaking broadly you can divide recursive algorithms up into two kinds:

* Divide and conquer
* Incremental

A divide and conquer algorithm is one that breaks a problem up into large subcomponents and solves each independently.  A good example would be [mergesort](https://en.wikipedia.org/wiki/Merge_sort), where at each step it breaks the data in half.  If at each step you break the data in half you won't ever need more than log2 calls to your recursive function.  A million elements?  Feh: twenty calls is nothing.  A trillion?  Feh: forty calls is nothing.  If your algorithm is a good divide and conquer — and mergesort is the canonical example of a good divide and conquer — then go to town with your bad self and use recursion with wild abandon.

But there are other algorithms, too, which only do a tiny little bit of the problem at each step.  We call these _incremental_ recursive methods.  Our maze solving algorithm is a good example: at each step we only discover the next step towards the maze.  If the route to the maze has 500 steps, we're going to make 500 calls, and at some point we're going to exhaust the stack and our program will blow up.

The really annoying part comes from algorithms which are sometimes well-behaved D&C, and sometimes poorly-behaved incremental.  For instance, [quicksort](https://en.wikipedia.org/wiki/Quick_sort) is normally considered a well-behaved D&C algorithm.  But if you feed it data that's already in sorted order, it turns into an incremental algorithm.  This is why everyone who writes quicksort either (a) avoids writing it in a recursive style, or (b) randomizes the input before running the algorithm to reduce the likelihood there's any order in the input.

## A general rule

* Prototype recursively, deploy iteratively.
* Only deploy iterative code if you've carefully considered the risks of stack exhaustion

## The challenge

So.  As already mentioned, our maze traverser is an example of an iterative recursive algorithm.  The Minotaur can make it blow sky-high by giving it a large maze.  To resolve this bug and make it possible to run this on enormous input sets, we'll convert it from a recursive function into an iterative function.

Before reading further, try to do it yourself.  It's a surprisingly difficult task if you haven't done it before.  Don't be afraid to ask for help.

## The solution

Beyond a trivial change to our `import` statement, our changes are all in the `depthfirst` function.

```python
def depthfirst(start: str, finish: str) -> str:
    """Uses slightly less naïve depth-first search to find a 
    route out of the Minotaur's maze."""
```

Already we see we're down one variable.  We used `rope` to pass data from one stack frame to the next.  Since we're no longer putting things onto the stack, we don't need `rope`.

Note that we also corrected the docstring.  We were never guaranteeing an optimal result, only _a_ result.

Did you notice that in Iteration 1 we failed to fully use type hints?  We didn't bother to give a type hint for the return value, for starters.  This is okay!  In early stages of development it can be a great help to not worry about typing and just get the algorithm running.  But as development continues, it's a good idea to start using type hints: it's a way to help the compiler flag problems before they happen.

In Python, a bare declaration is a no-op.  Variables do not become real until they are instantiated.  So when we create a block of variable declarations — in order to get all the type hinting in one place — we also initialize everything.

```python
    stack: List[List[str, List[str]]] = [[start, list(_MAZE[start])]]
    current_room: str = ""
    first_portal: str = ""
    portals: List[str] = []
    visited: List[str] = []
```

I kind of lied about how we're not putting things onto the stack.  We totally are, and anyone who says this iterative code doesn't use a stack is lying to you.  It's just that this stack is one we maintain ourselves and we store it off in the vast space of userland.

The Python interpreter's built-in stack can only handle a few hundred frames before exhausting.  But this userland stack can grow enormously: I've got 32GiB of RAM on this laptop.

Python uses square brackets to denote a list.  We're using a list as our stack.  Each of our simulated stack frames is a list containing a room (a key in `_MAZE`) and a list of unvisited exits.

```python
    while stack:
```

Since our stack is just a Python list, we can use some Python shorthand.  Empty lists, when evaluated in a boolean context, are considered `False`.  We could have written this as `while len(stack) > 0`, `while len(stack)`, `while stack != []`, or many other different ways: but just `while stack` will work.  So long as we have stack frames, we'll keep running.

```python
        current_room, portals = stack[-1]
```

Python also supports _multiple assignment_.  If the right-hand side of an assignment is a list or a tuple (a const list, basically), you can assign each member of the list to a different variable all at once.  Here, we use multiple assignment to unpack the final stack frame into `current_room` and `portals`.

You may be confused by the `-1` used as an index.  Python has a lovely feature where positive indices are normal zero-offset indices from the beginning of a list, but negative indices are one-offset from the _end_ of a list.  So `stack[-1]` is really just a terse way of getting the final stack frame.

```python
        visited = [X[0] for X in stack]
        portals = [X for X in portals if X not in visited]
        stack[-1] = [current_room, portals]
```

The very first thing we do is use a clever list comprehension to figure out where we've already been.  We iterate over `stack`, calling each element `X`, and collect the first element `X[0]` out of it.

The next thing we have to do is ensure we're not going to get into any loops.  Since we know where we've been, we use another list iteration to exclude from consideration any portals leading to places we've been.

Finally, we update our final stack frame to reflect the processing we've done.

```python
        if current_room == finish:
            break
        if not portals:
            stack = stack[:-1]
            continue
```

The first part of this should be fairly obvious: if we're done, we're done!  And if we're not done, and we have no more portals we can move through, then we say "to hell with this place" and walk back to the room before us — which we can simulate by dropping the final stack frame.


```python
        first_portal = portals[0]
        stack[-1] = [current_room, portals[1:]]
        stack.append([first_portal, list(_MAZE[first_portal])])
```
The preceding `if` statements all led to the `while` loop either breaking out or resuming.  We could have structured these three clauses as an `if/elif/else`, but I personally find this more readable: if X, return, if Y, continue, otherwise, fallthrough to the block below.

Our `first_portal = portals[0]` line is guaranteed to always work: if we don't have at least one portal, we'd bail out in the clause above.

In our next line, we adjust our current (final) stack frame.  Instead of being `[current_room, portals]`, it's `[current_room, portals[1:]]`.  The colon syntax indicates a _list slice_.  A slice from X to X is written as `slice[X:Y]`, and is a half-open sequence starting at X and running up to, but not including, Y.  Attempting to slice off the end of a list is all right: it just gives you an empty list.

So, why do we slice?  Because we're about to explore a new room, and we want to do the equivalent of mark an X over the door.  By removing it from our list of exits we guarantee we will never consider it again.

Finally, we add a new stack frame consisting of the portal we're going through, and all the exits that can be reached from that portal.

Once we've done that, we repeat our loop.  This time, we start our inquiry by looking at the newly-added stack frame.

```python
    return ''.join([X[0] for X in stack])
```

And here we introduce _just a touch_ of object orientation.  The empty string (which can be represented with either two single quotes or two double quotes, Python doesn't care) is a full-fledged string object, and has all the methods any string object has.  The `.join` method of a string object takes a list of strings, and returns a single string of the string list joined together with the string object. `', and spam, and '.join(["ham", "eggs"])` would give `ham, and spam, and eggs`.  Were we to do the same to `["ham", "eggs", "pineapple"]` we'd get `ham, and spam, and eggs, and spam, and pineapple`.

By using an empty list, we take a list of letters and glue them together with nothing between them — making a neat string out of it.

## Try it!

Try running this code.  Verify for yourself that it works.  Then start asking yourself the same question:

_How can I blow it up?_
