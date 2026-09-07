# Current contract
The [confirmed stop request](STOP_REQUEST.md) supersedes continuation in the
[occupied-cell request](OCCUPIED_REQUEST.md). Implementation is pending; the
[original request](ORIGINAL.md) and prior confirmations remain preserved.

Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. An attempted unknown command raises ValueError. No persistence
or pathfinding. Occupied cells are fixed coordinates supplied by the caller.

An occupied forward target reports False, preserves position and heading at that
command, and immediately stops the batch. Return that pose and outcomes through
the failed command, including earlier successes. Earlier moves are not rolled back.
Later commands are not attempted and have no outcomes. With no blocked move,
process the batch normally and return one success per valid command.

See [current acceptance examples](DESIGN.md#acceptance) for exact results.
