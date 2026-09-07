# Movement design D2
Status: author-proposed correction to R1; awaiting review.
For F, calculate the adjacent target. If occupied, assign x/y to that target,
retain the original heading and emit False. Otherwise assign target and emit True.
Continue accepting later commands. Turns affect heading in place.
