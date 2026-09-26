# Debugging Practical — Worker State Machine — Overtraining Edition

        **Recommended time box:** 90 minutes  
        **Difficulty:** Intentionally harder and larger than the reported interview exercises

        ## Scenario

        A worker control plane handles registration, draining, leases, failures, heartbeats, and recovery. Out-of-order events expose invalid transitions and lost work.

        The public interfaces and test expectations are already consumed by other systems. Diagnose the behavior and make the tests pass with small, focused changes. Do not replace the architecture or weaken assertions.

        ## Run the exercise

        ```bash
        python3 -m unittest discover -s tests -v
        ```

        Failing assertions are expected in the starter state. Import and syntax errors are not.

        ## Skills under pressure

        - finite-state reasoning
- event idempotency
- lease recovery
- out-of-order updates

        ## Interview constraints

        - Preserve public names and function signatures.
        - Start from a failing behavior and trace only the relevant execution path.
        - Make one hypothesis and one targeted change at a time.
        - Rerun the narrowest relevant test, then the full suite.
        - Remove temporary debug output before finishing.

        This is an original practice reconstruction based on public interview descriptions. It is not an official Scale AI repository and contains no proprietary interview material or answer key.
