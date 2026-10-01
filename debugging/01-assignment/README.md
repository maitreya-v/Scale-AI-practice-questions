# Assignment pipeline

**Time box:** 45–60 minutes. **Seeded defects:** 8.

Contributors have completed course IDs. Projects have a priority (larger means more urgent), capacity, and a set of required course IDs. Load contributors from a CSV whose `courses` cell uses `|` between IDs. A contributor is eligible when unassigned and all prerequisites are met; a project with no prerequisites is open to anyone. Assign each contributor at most once, handling higher priority projects first and preserving contributor input order within each project. Each call to `assign` recomputes assignments, even if the same objects were used before. `report` must list only people left unassigned.

Run `python3 -m unittest discover -s tests -v` from this directory. Fix the behavior without changing public signatures or weakening tests. No external services are needed.
