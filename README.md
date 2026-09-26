# Debugging Practical — API Data Pipeline — Overtraining Edition

        **Recommended time box:** 90 minutes  
        **Difficulty:** Intentionally harder and larger than the reported interview exercises

        ## Scenario

        A file-to-JSON classification pipeline must validate records, contain per-row failures, preserve order, retry transient model errors, and write only beneath an allowed directory.

        The public interfaces and test expectations are already consumed by other systems. Diagnose the behavior and make the tests pass with small, focused changes. Do not replace the architecture or weaken assertions.

        ## Run the exercise

        ```bash
        python3 -m unittest discover -s tests -v
        ```

        Failing assertions are expected in the starter state. Import and syntax errors are not.

        ## Skills under pressure

        - boundary validation
- partial failure handling
- retry semantics
- safe paths and ordering

        ## Interview constraints

        - Preserve public names and function signatures.
        - Start from a failing behavior and trace only the relevant execution path.
        - Make one hypothesis and one targeted change at a time.
        - Rerun the narrowest relevant test, then the full suite.
        - Remove temporary debug output before finishing.

        This is an original practice reconstruction based on public interview descriptions. It is not an official Scale AI repository and contains no proprietary interview material or answer key.
