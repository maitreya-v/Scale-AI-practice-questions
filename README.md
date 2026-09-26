# Debugging Practical — Async Concurrency — Overtraining Edition

        **Recommended time box:** 90 minutes  
        **Difficulty:** Intentionally harder and larger than the reported interview exercises

        ## Scenario

        An asynchronous fan-out service must bound parallel work, preserve input order, isolate failures, honor timeouts, and propagate cancellation.

        The public interfaces and test expectations are already consumed by other systems. Diagnose the behavior and make the tests pass with small, focused changes. Do not replace the architecture or weaken assertions.

        ## Run the exercise

        ```bash
        python3 -m unittest discover -s tests -v
        ```

        Failing assertions are expected in the starter state. Import and syntax errors are not.

        ## Skills under pressure

        - task lifecycle
- semaphore scope
- ordering
- timeouts and cancellation

        ## Interview constraints

        - Preserve public names and function signatures.
        - Start from a failing behavior and trace only the relevant execution path.
        - Make one hypothesis and one targeted change at a time.
        - Rerun the narrowest relevant test, then the full suite.
        - Remove temporary debug output before finishing.

        This is an original practice reconstruction based on public interview descriptions. It is not an official Scale AI repository and contains no proprietary interview material or answer key.
