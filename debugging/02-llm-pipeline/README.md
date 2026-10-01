# Silent model output

**Time box:** 45–60 minutes. **Seeded defects:** 8.

Trace a request through prompt construction, model versioned cache keys, a deterministic model call, response parsing, and batch handling. Prompts trim surrounding whitespace. A cache miss calls the model with the human-readable prompt; repeated identical requests reuse the result. Parse `CATEGORY=<value>` case insensitively and return lowercase `urgent`, `normal`, or `other`. Unknown responses become `other`. In a batch, a model failure becomes `other` for that item and later items still run in order.

Run `python3 -m unittest discover -s tests -v` from this directory. Preserve public signatures. The model is local and needs no API key.
