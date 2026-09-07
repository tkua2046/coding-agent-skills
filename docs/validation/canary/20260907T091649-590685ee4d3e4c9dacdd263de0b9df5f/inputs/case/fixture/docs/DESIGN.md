# Current design
The caller reads data/active.json and loads the selected v1 file. Stable IDs are
unique; duplicate IDs are errors. No migration or recovery protocol exists yet.
