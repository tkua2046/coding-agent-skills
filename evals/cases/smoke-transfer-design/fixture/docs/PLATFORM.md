# Supplied local storage contract

Synthetic platform contract for this fixture, version 1; this is a task assumption, not a quoted OS manual or a claim about all filesystems.

The supported adapter writes a temporary file beside config.json, closes it, and replaces config.json within that directory. A completed replacement exposes the entire new file; a failed replacement leaves the prior destination intact. Process interruption before replacement can leave a temporary file. A retry must ignore or replace that unfinished temporary file and validate the complete input before activation.

This contract covers process interruption and reported I/O failure on the local adapter. It does not establish power-loss durability, concurrent writers, cross-filesystem moves, remote storage, or the behavior of a different primitive. State any additional assumptions or unresolved durability requirement.
