# Iteration 1

In our first iteration of depth-first search, we're going to use an old familiar example: walking a maze!

If I were to strand you in the Labyrinth of Crete, you could navigate it just fine if I were to let you bring in a rope and a piece of chalk.  You'd start off in the first area of the maze and you'd be trying to get to an exit.  You know what the exit looks like, but you don't know how to get there.

Getting to the exit is a three step process.  First, are you standing in front of the exit?  Then cry glory hallelujah, because you're done.  (One step ahead of the Minotaur, no doubt.)

If you're not that lucky, then you still need to navigate the maze.  Look at each exit in turn.  Is there a rope in the area beyond?  Then write a big X over that exit: you've been there before.  This keeps us from getting caught in circles.

Pick an exit, any exit, from the ones that don't have Xes over top.  (You might think "any exit" means "pick a random exit".  No, it means "I don't care which you take".)  Spool out some rope and step through, marking an X over top of the door as you go through.

It may be the case that you don't have any exits, though!  In that case, you follow the rope back to the room you came from and repeat the process from scratch.  You remembered to mark an X over the top of this doorway, though, so you're assured you're not going to go this way again.

As simple as this solution sounds, it's guaranteed that you will always, always, always, find an exit if one exists.  Unfortunately, there are no guarantees about how _fast_ this algorithm runs, and the Minotaur of Crete is hunting you.

This is a good beginning.  We can do better.  Study the code and see how we're able to start from point A in the maze and move to point T.

In the next iteration we're going to reveal the trick the Minotaur is using to keep you in the maze.  You're not done with him yet.

## Code walkthrough

```python
#!/usr/bin/env python3
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


```

In modern Python style, the script starts with a hashbang leading to the Python script.  Let me give you a bit of guidance from twenty years of Python programming: _don't hardcode the path._  It's easy for a system to have several different Python executables of different versions lying about.  Your code will be the most portable if, instead of hardcoding a path, you use the system `env` command to find the correct path for you.

In Python 3, any program without a `# coding` line is assumed to be in UTF-8.  So, strictly speaking, this line is unnecessary.  Most Python programmers will include it anyway, and so it's included here out of respect for community convention.

A well-written Python program will always, _always,_ have a triply-quoted string immediately after the first two lines.  This triply-quoted string describes the purpose of the program well enough for someone to get the gist without needing to read your source code.  The documentation block should not document how the program works, only what it does and possibly why it's needed.

Following that, let's run on to:

```python

from typing import Dict

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

```

You may have heard that Python is a typeless programming language.  That's not true and has never been true: things in Python have extremely strong type checking.  It's just that the type checking is all done behind-the-scenes at runtime.  Most programmers think that if they don't see something happening it's not being done, which is how the myth of 'typeless' Python came to be.

You can still write that sort of code today, although it's considered to be in poor form.  There's a time and a place for static type checking.  In Python 3.6 and later it's considered to be good form to use static type checking whenever possible in order to improve the safety and reliability of your code.  Since our goal here is to follow good practice, we're going to use static typing wherever practical.

But, if you find yourself deeply allergic to it, you don't _have_ to.  It's just recommended.

More in the realm of Python customs: anything declared at file scope that's intended to be a constant is written in uppercase.  Once again, this is only custom.  You may break this rule if needed.  Since our maze is a file-scope constant, it's declared in uppercase.

Finally, by default Python makes it easy for other Python code to introspect into your code and discover all its fiddly bits.  Variables and functions that have their names prefixed with an underscore are exempt: these are considered "for internal use only" and not made available.  (You can still get at them, of course: it just takes more work.)

So: our `_MAZE` is a constant local to this file, and we give the Python environment a strong hint that it should map strings to strings.  If the Python environment sees us doing something wild like storing integers in our dictionary, it will complain to us.

In our `_MAZE`, each key represents a location in the maze, and each value represents where one can go from this location.  The technical term for this sort of value is an _adjacency list,_ and you might see them called such in the future.

With this out of the way, let's continue!

```python
def depthfirst(current: str, finish: str, rope: str=""):
    """Uses naïve depth-first search to find an optimal route
    out of the Minotaur's maze."""
```

Python methods are (almost) always defined with `def`, and modern style includes type annotations if possible.  The absence of an initial underscore means that other Python code is allowed to import this function, should it need a depth-first search tool.

Note the letter `ï`.  Unicode is a first-class citizen in Python: it can be used in docstrings, in identifiers, anywhere it makes sense.

And finally, notice the docstring.  I'm sure by now you understand the importance of documenting your code: I won't belabor the point further.

```python
    rope += current
```

Our `rope` starts off life as an empty string.  It has no record of where we've been.  Whichever room of the maze we're in, we're going to add it to the rope.

```python
    if current == finish:
        return rope
```

If we're done, then we're done.  The `rope` has a record of our path through the maze: we return it and that's our exit.

But what if we're not done?

```
    portals = [X for X in _MAZE[current] if X not in rope]
```

The right-hand side of that is called a _list comprehension._  You'll see them frequently in Python code.  It's pretty much equivalent to:

```python
portals = []
for portal in _MAZE[current]:
    if portal not in rope:
        portals.append(portal)
```

The reason why we prefer list comprehensions is because the notation is cleaner and it optimizes like all bloody hell.  However, it's easy to turn list comprehensions into baroque monstrosities that are impossible for newcomers to read.  Keep them clean and simple, please.

Once we have our list of unvisited portals, we go through them one at a time hoping to find an exit:

```python
    for portal in portals:
        route = depthfirst(portal, finish, rope)
        if route:
            return route
```

"But wait," you might ask: "why didn't you use a list comprehension?"

A list comprehension, by its nature, has no break-out mechanism.  Whatever process you're doing on the list will be done on the _entire_ list before you receive a single result.  This isn't what we want to do with our maze.  We want to bail out the moment we discover a way out.

We could have replaced those lines with this instead:

```python
return [depthfirst(X, finish, rope) for X in _MAZE[current]]
```

But that would be:

* slower (since we'd be checking every exit)
* much more difficult to read
* would require subtle changes to the rest of the code

Not every instance of brevity is wit.

```python
    return None
```

If we didn't find the exit, then shrug and give up without signaling to the layer above us in the call stack that we found anything.

And then, finally, the _piéce de resistance:_

```python
if __name__ == '__main__':
    print(depthfirst("A", "T"))
```

Identifiers with double underscores before and behind them are special internal variables.  "Special," as far as we're concerned, means "treat them as read-only until you fully understand the chainsaw you're juggling."

Each Python module has a special name, which is normally the same as the name of the file containing it on the hard drive.  The exception is the module which launches the program, which gets its `__name__` reset to the string `__main__`.

In other words: if we're being imported by another Python program, maybe because it needs a depth-first search algorithm, then we're not going to execute this block.  But if we're launching this Python program at the command line, we'll execute the line `print(depthfirst("A", "T"))`.

Try it for yourself.  Does it find a valid path through the maze?

Can you construct inputs that will make this blow up, or make it cease being useful?
