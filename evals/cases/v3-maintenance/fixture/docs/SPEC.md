# Current behavior
Unbounded grid, integer coordinates, clockwise headings 0 through 3. F advances;
L/R turn in place. Unknown commands raise ValueError. No persistence or pathfinding.
Occupied forward targets report False, preserving pose; the batch continues.
