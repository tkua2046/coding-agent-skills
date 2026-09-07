1. **Behavior changing:** Runs gain optional occupied coordinates. A forward move into an occupied cell returns `False`, preserves position and heading, and allows later commands to continue. Preserve existing two-argument calls and return shape, successful moves and turns returning `True`, unknown commands raising `ValueError`, and occupancy remaining local to each call.

2. **Main technical decision:** Propose `run(pose, commands, occupied=())` with an immutable occupancy snapshot taken once per run. Check the destination before assigning the new pose. This supports generators, collapses duplicates, and prevents caller mutations from changing occupancy during execution. The tradeoff is O(k) setup time and storage for expected constant-time membership checks.

3. **Next uncompleted outcome:** Deliver optional fixed occupancy in `navigator.run`, regression tests, and updated README and current SPEC documentation together. This depends on the proposed D1 amendment and API clarifications, with pending document-review changes resolved before affected choices are implemented. A decisive acceptance example is:
   - Start: `(0, 0, 0)`
   - Commands: `FFRF`
   - Occupied: `{(0, 1)}`
   - Expected: `((1, 0, 1), [False, False, True, True])`

The excerpts say implementation belongs to a later task and reviews remain pending. They supply no completed implementation or test results. This first-screen comprehension result is not human usability proof.