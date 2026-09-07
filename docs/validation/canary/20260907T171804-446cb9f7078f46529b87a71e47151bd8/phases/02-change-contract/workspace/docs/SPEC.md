# Current contract

The [confirmed stop request](STOP_REQUEST.md) supersedes continuation after a
blocked forward move. This is the target contract; implementation is pending.
The [original request](ORIGINAL.md) and [occupied-cell request](OCCUPIED_REQUEST.md)
remain preserved sources; only the latter's continuation behavior is superseded.

Unbounded grid, integer coordinates, clockwise headings 0 through 3 (north, east,
south, west). A caller supplies pose, commands and optional fixed occupied cells.
F advances one cell; L/R turn in place. Successful commands report True.
No persistence, pathfinding, moving obstacles or configuration file.

An occupied forward target reports False and stops the command batch immediately.
Return the pose immediately before that failed command, preserving position and
heading, and outcomes through that command, including its False. Earlier successful
moves and turns remain applied. Do not attempt later commands or emit outcomes for
them. An attempted unknown command raises ValueError; an unknown command after a
blocked F is not attempted and does not raise.

For concrete acceptance inputs and outputs, see [design acceptance](DESIGN.md#acceptance).
