# Bugfix

**STOP.**  Try to resolve the bug first before relying on this solution.  Wrestle with the problem for a while but stop before you get frustrated.

## History

* [Installment 1](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/1)
* [Installment 2](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/2)
* [Installment 3](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/3)
* [Installment 4](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/4)
* [Installment 5](https://github.com/rjhansen/pluspora-algo/tree/master/depthfirst/dev/5)

## The problem

Imagine this very small maze:

```
+-+-+
|0 1|
+ + +
|2 3|
+-+-+
```

To get from 0 to 3 there are two routes, `0-1-3` and `0-2-3`.  Yet, our algorithm reports each of those routes twice.  Why?

Let's look at the code:

```python
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
```

Playing around with it and littering it with `print` calls to dump the stack lead us quickly to the offending portion:

```python
if current_room == finish:
    yield visited
if not portals:
    stack = stack[:-1]
    continue
first_portal = portals[0]
stack[-1] = (current_room, portals[1:])
stack.append((first_portal, graph[first_portal]))
```

If we're in the finish room, we `yield`.  The next iteration begins on the next line (`if not portals`).  Assume this `if` doesn't get tripped.  Execution then continues on the line starting with `first_portal`.

Hmm.  Let's look at that code again, this time in a more human-readable way:

```
[do something if we found the exit]
[do something if we're in a dead end]
[continue exploring from here]
```

So, if we found the exit we `yield` it, and on the next invocation we're assuming we skip over the dead-end code, so… wait…

If we found the exit, _we continue exploring from there?!_

And suddenly all becomes clear.  Let's say there's a room beyond the exit we could still get to.  We enter the room with the exit, realize we're in the exit, and scream "hey, found it!".  Then we append the next room to our stack and walk into it.  It's a dead-end, so we walk out, pop the stack, and discover we're back in the room with the exit.  "Hey, found it!" we call out.  Depending on how much exploration we can do beyond the exit, we might report this route many times!

The solution is clean and neat:

```python
if current_room == finish:
    yield visited
    stack = stack[:-1]
    continue
```

Now the logic is, "if we find the exit `yield` it; and on our next invocation, walk into the prior room and resume exploration from there."

## Conformance

### pylint

No errors and full marks.

### pycodetest

No errors and full marks.

### mypy

No errors and full marks.

### pytest

No errors.