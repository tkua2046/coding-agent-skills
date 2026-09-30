# Accepted D3: stop after blocked forward movement
The owner confirmed the revised public batch contract. A blocked F preserves pose,
returns False, and terminates this batch; later commands are not attempted.
At (0,0,N), obstacle (0,1), FRF returns (0,0,N), [False]. Turns and unblocked moves
retain prior behavior. D2 continuation is historical, retained in history/D2.md.
Implementation has not adopted D3. Update the API before enabling the text adapter.
